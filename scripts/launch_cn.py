
import json, os, sys

# ── 加载中文翻译 ──
_zh_path = os.path.join(os.path.dirname(__file__), "..", "locale", "zh_CN.json")
_zh_dict = {}
if os.path.exists(_zh_path):
    with open(_zh_path, "r", encoding="utf-8-sig") as f:
        _zh_dict = json.load(f)

def _tr(text):
    """翻译单个字符串，优先精确匹配，其次模糊匹配"""
    if not text or not isinstance(text, str):
        return text
    if text in _zh_dict:
        return _zh_dict[text]
    # 尝试去除前后空格和冒号后匹配
    stripped = text.strip().rstrip(':').rstrip('.')
    if stripped in _zh_dict:
        return text.replace(stripped, _zh_dict[stripped])
    return text

if _zh_dict:
    import customtkinter as ctk
    import tkinter as tk

    # ── 1. patch __init__ ──
    _orig_btn_init = ctk.CTkButton.__init__
    _orig_label_init = ctk.CTkLabel.__init__
    _orig_check_init = ctk.CTkCheckBox.__init__
    _orig_radio_init = getattr(ctk.CTkRadioButton, "__init__", None)
    _orig_switch_init = getattr(ctk.CTkSwitch, "__init__", None)
    _orig_frame_init = getattr(ctk.CTkFrame, "__init__", None)
    _orig_entry_init = getattr(ctk.CTkEntry, "__init__", None)
    _orig_option_init = getattr(ctk.CTkOptionMenu, "__init__", None)
    _orig_combo_init = getattr(ctk.CTkComboBox, "__init__", None)
    _orig_tab_init = getattr(ctk.CTkTabview, "__init__", None)

    def _patch_init(orig_init):
        def _wrapped(self, master=None, **kwargs):
            if 'text' in kwargs:
                kwargs['text'] = _tr(kwargs['text'])
            if 'placeholder_text' in kwargs:
                kwargs['placeholder_text'] = _tr(kwargs['placeholder_text'])
            # 保存原始值列表，用于后续修正默认选中项
            _orig_values = list(kwargs.get('values', [])) if isinstance(kwargs.get('values'), list) else None
            if 'values' in kwargs and isinstance(kwargs['values'], list):
                kwargs['values'] = [_tr(v) for v in kwargs['values']]
            orig_init(self, master, **kwargs)
            # 修正：如果默认选中值仍是未翻译的英文，替换为中文
            if _orig_values and hasattr(self, 'get') and hasattr(self, 'set'):
                try:
                    cur = self.get()
                    if cur in _orig_values:
                        idx = _orig_values.index(cur)
                        if idx < len(kwargs.get('values', [])):
                            self.set(kwargs['values'][idx])
                except Exception:
                    pass
        return _wrapped

    ctk.CTkButton.__init__ = _patch_init(_orig_btn_init)
    ctk.CTkLabel.__init__ = _patch_init(_orig_label_init)
    ctk.CTkCheckBox.__init__ = _patch_init(_orig_check_init)
    if _orig_radio_init:
        ctk.CTkRadioButton.__init__ = _patch_init(_orig_radio_init)
    if _orig_switch_init:
        ctk.CTkSwitch.__init__ = _patch_init(_orig_switch_init)
    if _orig_frame_init:
        ctk.CTkFrame.__init__ = _patch_init(_orig_frame_init)
    if _orig_entry_init:
        ctk.CTkEntry.__init__ = _patch_init(_orig_entry_init)
    if _orig_option_init:
        ctk.CTkOptionMenu.__init__ = _patch_init(_orig_option_init)
    if _orig_combo_init:
        ctk.CTkComboBox.__init__ = _patch_init(_orig_combo_init)
    if _orig_tab_init:
        ctk.CTkTabview.__init__ = _patch_init(_orig_tab_init)

    # ── 2. patch .configure() for all CTk widgets ──
    def _patch_configure(cls, orig_configure):
        def _wrapped(self, **kwargs):
            if 'text' in kwargs:
                kwargs['text'] = _tr(kwargs['text'])
            if 'placeholder_text' in kwargs:
                kwargs['placeholder_text'] = _tr(kwargs['placeholder_text'])
            if 'title' in kwargs:
                kwargs['title'] = _tr(kwargs['title'])
            if 'values' in kwargs and isinstance(kwargs['values'], list):
                kwargs['values'] = [_tr(v) for v in kwargs['values']]
            return orig_configure(self, **kwargs)
        return _wrapped

    for cls in [ctk.CTkButton, ctk.CTkLabel, ctk.CTkCheckBox, ctk.CTkRadioButton,
                ctk.CTkSwitch, ctk.CTkFrame, ctk.CTkEntry, ctk.CTkOptionMenu,
                ctk.CTkComboBox, ctk.CTkTabview, ctk.CTkTextbox,
                ctk.CTkScrollableFrame, ctk.CTkProgressBar, ctk.CTkSegmentedButton]:
        if hasattr(cls, 'configure'):
            cls.configure = _patch_configure(cls, cls.configure)

    # ── 3. patch tkinter .config() ──
    _orig_tk_label_config = tk.Label.config
    _orig_tk_button_config = tk.Button.config
    _orig_tk_check_config = tk.Checkbutton.config
    _orig_tk_radio_config = tk.Radiobutton.config
    def _tk_config_wrapper(orig):
        def _wrapped(self, **kwargs):
            if 'text' in kwargs:
                kwargs['text'] = _tr(kwargs['text'])
            return orig(self, **kwargs)
        return _wrapped
    tk.Label.config = _tk_config_wrapper(_orig_tk_label_config)
    tk.Button.config = _tk_config_wrapper(_orig_tk_button_config)
    tk.Checkbutton.config = _tk_config_wrapper(_orig_tk_check_config)
    tk.Radiobutton.config = _tk_config_wrapper(_orig_tk_radio_config)

    # ── 4. patch StringVar.set() ── 注意：不翻译枚举值，只翻译已知UI文本
    # (移除 StringVar patch，枚举值如 Epoch/Never/Minutes 不能翻译)

# ── 覆盖窗口标题 ──
import customtkinter as _ctk
_orig_ctk_init = _ctk.CTk.__init__
def _patched_ctk_init(self, *args, **kwargs):
    _orig_ctk_init(self, *args, **kwargs)
    self.title("OneTrainer-AMD显卡机智启动器专用版-B站：机智罗_LX")
_ctk.CTk.__init__ = _patched_ctk_init

from train_ui import main
main()
