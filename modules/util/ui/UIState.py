import tkinter as tk
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from modules.util.config.BaseConfig import BaseConfig
from modules.util.type_util import issubclass_safe

# ═══════════════════════════════════════════
# 🔄 汉化反向映射：中文 → 英文 Enum 键
# UI 显示中文，Model 层接收英文——MVC 架构正确姿势
# 有新词条 KeyError 时在此追加即可
# ═══════════════════════════════════════════
REVERSE_I18N_MAP = {
    # ── 时间单位 ──
    '秒': 'SECOND', '分钟': 'MINUTE', '小时': 'HOUR',
    # ── 训练周期/触发 ──
    '轮次': 'EPOCH', '步数': 'STEP', '从不': 'NEVER', '永不': 'NEVER', '始终': 'ALWAYS', '总是': 'ALWAYS',
    # ── 状态/开关 ──
    '无': 'NONE', '标准': 'STANDARD', '验证': 'VALIDATION', '确定': 'ok',
    # ── 调度器 ──
    '恒定': 'CONSTANT', '线性': 'LINEAR', '余弦': 'COSINE',
    # ── 批次模式 ──
    '批次': 'BATCH', '全局批次': 'GLOBAL_BATCH', '双向': 'BOTH', '全局双向': 'GLOBAL_BOTH',
    # ── 梯度累积 ──
    '梯度累积': 'GRADIENT_ACCUMULATION',
    # ── 概念类型 ──
    '概念': 'concepts', 'Prior预测': 'PRIOR_PREDICTION', '预测': 'PRIOR_PREDICTION',
    # ── 大小写模式 ──
    '全大写': 'capslock', '首字母大写': 'title', '句首大写': 'first', '随机': 'random',
    # ── 噪声调度 ──
    'P2': 'P2',
    # ── 采样 ──
    '最小SNR伽马': 'MIN_SNR_GAMMA', '去偏估计': 'DEBIASED_ESTIMATION',
    # ── 注意力 ──
    '注意力-MLP': 'attn-mlp', '仅注意力': 'attn-only',
    # ── 其他 ──
    '完整': 'full', '基础': 'basic', '自定义': 'CUSTOM',
    '重复次数': 'repeats', '重复': 'repeats',
}

# ═══════════════════════════════════════════
# 🔄 正向映射：英文 Enum 键 → 中文显示
# 加载配置时，将后端英文值翻译为中文显示在 UI 上
# ═══════════════════════════════════════════
FORWARD_I18N_MAP = {v: k for k, v in REVERSE_I18N_MAP.items()}
for _k, _v in list(FORWARD_I18N_MAP.items()):
    FORWARD_I18N_MAP[_k.lower()] = _v
# ═══════════════════════════════════════════
# ═══════════════════════════════════════════


class UIState:
    __vars: dict[str, Any]
    __var_traces: dict[str, dict[int, Callable[[], None]]]
    __latest_var_trace_id: int

    def __init__(self, master, obj):
        self.master = master
        self.obj = obj

        self.__var_types: dict[str, type] = {}
        self.__var_nullables: dict[str, bool] = {}
        self.__var_defaults: dict[str, Any] = {}

        self.__vars = self.__create_vars(obj)
        self.__var_traces = {name: {} for name in self.__vars}
        self.__latest_var_trace_id = 0

    def update(self, obj):
        self.obj = obj
        self.__set_vars(obj)

    def get_var(self, name):
        split_name = name.split('.')

        if len(split_name) == 1:
            return self.__vars[split_name[0]]
        else:
            state = self
            for name_part in split_name:
                state = state.get_var(name_part)
            return state

    def add_var_trace(self, name, command: Callable[[], None]) -> int:
        self.__latest_var_trace_id += 1
        self.__var_traces[name][self.__latest_var_trace_id] = command
        return self.__latest_var_trace_id

    def remove_var_trace(self, name, trace_id):
        self.__var_traces[name].pop(trace_id)

    def remove_all_var_traces(self, name):
        self.__var_traces[name] = {}

    def __call_var_traces(self, name):
        for trace in self.__var_traces[name].values():
            trace()

    def __set_str_var(self, obj, is_dict, name, var, nullable):
        if is_dict:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    obj[name] = None
                else:
                    obj[name] = string_var
                self.__call_var_traces(name)
        else:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    setattr(obj, name, None)
                else:
                    setattr(obj, name, string_var)
                self.__call_var_traces(name)

        return update

    def __set_enum_var(self, obj, is_dict, name, var, var_type, nullable):
        if is_dict:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    obj[name] = None
                else:
                    obj[name] = self._resolve_enum(var_type, string_var, name)
                self.__call_var_traces(name)
        else:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    setattr(obj, name, None)
                else:
                    setattr(obj, name, self._resolve_enum(var_type, string_var, name))
                self.__call_var_traces(name)

        return update

    @staticmethod
    def _resolve_enum(var_type, string_var, name):
        """先反向映射中文→英文键，再查找 Enum，失败则告警并 fallback"""
        key = REVERSE_I18N_MAP.get(string_var, string_var)
        try:
            return var_type[key]
        except KeyError:
            print(f"\n[架构告警] UIState 收到未知键值: '{string_var}' (字段: {name})，请添加到 REVERSE_I18N_MAP！\n")
            try:
                return var_type[list(var_type.__members__.keys())[0]]
            except Exception:
                return None

    def __set_bool_var(self, obj, is_dict, name, var):
        if is_dict:
            def update(_0, _1, _2):
                obj[name] = var.get()
                self.__call_var_traces(name)
        else:
            def update(_0, _1, _2):
                setattr(obj, name, var.get())
                self.__call_var_traces(name)

        return update

    def __set_int_var(self, obj, is_dict, name, var, nullable):
        if is_dict:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    obj[name] = None
                elif string_var == "inf":
                    obj[name] = int("inf")
                elif string_var == "-inf":
                    obj[name] = int("-inf")
                else:
                    try:
                        obj[name] = int(string_var)
                    except ValueError:
                        obj[name] = None
                self.__call_var_traces(name)
        else:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    setattr(obj, name, None)
                elif string_var == "inf":
                    setattr(obj, name, int("inf"))
                elif string_var == "-inf":
                    setattr(obj, name, int("-inf"))
                else:
                    try:
                        setattr(obj, name, int(string_var))
                    except ValueError:
                        setattr(obj, name, None)
                self.__call_var_traces(name)

        return update

    def __set_float_var(self, obj, is_dict, name, var, nullable):
        if is_dict:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    obj[name] = None
                elif string_var == "inf":
                    obj[name] = float("inf")
                elif string_var == "-inf":
                    obj[name] = float("-inf")
                else:
                    try:
                        obj[name] = float(string_var)
                    except ValueError:
                        obj[name] = None
                self.__call_var_traces(name)
        else:
            def update(_0, _1, _2):
                string_var = var.get()
                if (string_var == "" or string_var == "None") and nullable:
                    setattr(obj, name, None)
                elif string_var == "inf":
                    setattr(obj, name, float("inf"))
                elif string_var == "-inf":
                    setattr(obj, name, float("-inf"))
                else:
                    try:
                        setattr(obj, name, float(string_var))
                    except ValueError:
                        setattr(obj, name, None)
                self.__call_var_traces(name)

        return update

    def __create_vars(self, obj):
        new_vars = {}

        is_dict = isinstance(obj, dict)
        is_config = isinstance(obj, BaseConfig)

        if is_config:
            for name, var_type in obj.types.items():
                self.__var_types[name] = var_type
                self.__var_nullables[name] = obj.nullables.get(name, False)
                if hasattr(obj, "default_values"):
                    self.__var_defaults[name] = obj.default_values.get(name, None)

                obj_var = getattr(obj, name)
                if issubclass_safe(var_type, BaseConfig):
                    var = UIState(self.master, obj_var)
                    new_vars[name] = var
                elif var_type is str:
                    var = tk.StringVar(master=self.master)
                    var.set("" if obj_var is None else obj_var)
                    var.trace_add("write", self.__set_str_var(obj, is_dict, name, var, obj.nullables[name]))
                    new_vars[name] = var
                elif issubclass_safe(var_type, Enum):
                    var = tk.StringVar(master=self.master)
                    raw_val = "" if obj_var is None else str(obj_var)
                    var.set(FORWARD_I18N_MAP.get(raw_val, raw_val))
                    var.trace_add("write", self.__set_enum_var(obj, is_dict, name, var, var_type, obj.nullables[name]))
                    new_vars[name] = var
                elif var_type is bool:
                    var = tk.BooleanVar(master=self.master)
                    var.set(obj_var or False)
                    var.trace_add("write", self.__set_bool_var(obj, is_dict, name, var))
                    new_vars[name] = var
                elif var_type is int:
                    var = tk.StringVar(master=self.master)
                    var.set("" if obj_var is None else str(obj_var))
                    var.trace_add("write", self.__set_int_var(obj, is_dict, name, var, obj.nullables[name]))
                    new_vars[name] = var
                elif var_type is float:
                    var = tk.StringVar(master=self.master)
                    var.set("" if obj_var is None else str(obj_var))
                    var.trace_add("write", self.__set_float_var(obj, is_dict, name, var, obj.nullables[name]))
                    new_vars[name] = var
        else:
            iterable = obj.items() if is_dict else vars(obj).items()

            for name, obj_var in iterable:

                if isinstance(obj_var, str):
                    var = tk.StringVar(master=self.master)
                    var.set(obj_var)
                    var.trace_add("write", self.__set_str_var(obj, is_dict, name, var, False))
                    new_vars[name] = var
                elif isinstance(obj_var, Enum):
                    var = tk.StringVar(master=self.master)
                    raw_val = str(obj_var)
                    var.set(FORWARD_I18N_MAP.get(raw_val, raw_val))
                    var.trace_add("write", self.__set_enum_var(obj, is_dict, name, var, type(obj_var), False))
                    new_vars[name] = var
                elif isinstance(obj_var, bool):
                    var = tk.BooleanVar(master=self.master)
                    var.set(obj_var)
                    var.trace_add("write", self.__set_bool_var(obj, is_dict, name, var))
                    new_vars[name] = var
                elif isinstance(obj_var, int):
                    var = tk.StringVar(master=self.master)
                    var.set(str(obj_var))
                    var.trace_add("write", self.__set_int_var(obj, is_dict, name, var, False))
                    new_vars[name] = var
                elif isinstance(obj_var, float):
                    var = tk.StringVar(master=self.master)
                    var.set(str(obj_var))
                    var.trace_add("write", self.__set_float_var(obj, is_dict, name, var, False))
                    new_vars[name] = var

        return new_vars

    def __set_vars(self, obj):
        is_dict = isinstance(obj, dict)
        is_config = isinstance(obj, BaseConfig)
        iterable = obj.items() if is_dict else vars(obj).items()

        if is_config:
            for name, var_type in obj.types.items():
                obj_var = getattr(obj, name)
                if issubclass_safe(var_type, BaseConfig):
                    var = self.__vars[name]
                    var.__set_vars(obj_var)
                elif var_type is str:
                    var = self.__vars[name]
                    var.set("" if obj_var is None else obj_var)
                elif issubclass_safe(var_type, Enum):
                    var = self.__vars[name]
                    var.set("" if obj_var is None else str(obj_var))
                elif var_type is bool:
                    var = self.__vars[name]
                    var.set(obj_var or False)
                elif var_type in (int, float):
                    var = self.__vars[name]
                    var.set("" if obj_var is None else str(obj_var))
        else:
            for name, obj_var in iterable:
                if isinstance(obj_var, str):
                    var = self.__vars[name]
                    var.set(obj_var)
                elif isinstance(obj_var, Enum):
                    var = self.__vars[name]
                    var.set(str(obj_var))
                elif isinstance(obj_var, bool):
                    var = self.__vars[name]
                    var.set(obj_var)
                elif isinstance(obj_var, int | float):
                    var = self.__vars[name]
                    var.set(str(obj_var))

    # metadata api
    def _resolve_state_and_leaf(self, name: str):
        parts = name.split('.')
        state: UIState = self
        for part in parts[:-1]:
            state = state.get_var(part)
            if not isinstance(state, UIState):
                return None, None
        return state, parts[-1]

    @dataclass(frozen=True)
    class VarMeta:
        type: type | None
        nullable: bool
        default: Any

    def get_field_metadata(self, name: str) -> "UIState.VarMeta":
        state, leaf = self._resolve_state_and_leaf(name)
        if state is None:
            return UIState.VarMeta(None, False, None)
        return UIState.VarMeta(
            state.__var_types.get(leaf),
            state.__var_nullables.get(leaf, False),
            state.__var_defaults.get(leaf, None),
        )
