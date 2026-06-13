
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
    _orig_frame_init = getattr(ctk.CTkFrame, "__init__", None)
    _orig_entry_init = getattr(ctk.CTkEntry, "__init__", None)
    _orig_option_init = getattr(ctk.CTkOptionMenu, "__init__", None)
    _orig_tab_init = getattr(ctk.CTkTabview, "__init__", None)

    def _patch_init(orig_init):
        def _wrapped(self, master=None, **kwargs):
            if 'text' in kwargs:
                kwargs['text'] = _tr(kwargs['text'])
            if 'placeholder_text' in kwargs:
                kwargs['placeholder_text'] = _tr(kwargs['placeholder_text'])
            orig_init(self, master, **kwargs)
        return _wrapped

    ctk.CTkButton.__init__ = _patch_init(_orig_btn_init)
    ctk.CTkLabel.__init__ = _patch_init(_orig_label_init)
    ctk.CTkCheckBox.__init__ = _patch_init(_orig_check_init)
    if _orig_frame_init:
        ctk.CTkFrame.__init__ = _patch_init(_orig_frame_init)
    if _orig_entry_init:
        ctk.CTkEntry.__init__ = _patch_init(_orig_entry_init)
    if _orig_option_init:
        ctk.CTkOptionMenu.__init__ = _patch_init(_orig_option_init)
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
            return orig_configure(self, **kwargs)
        return _wrapped

    for cls in [ctk.CTkButton, ctk.CTkLabel, ctk.CTkCheckBox, ctk.CTkFrame,
                ctk.CTkEntry, ctk.CTkOptionMenu, ctk.CTkTabview, ctk.CTkTextbox,
                ctk.CTkScrollableFrame, ctk.CTkProgressBar]:
        if hasattr(cls, 'configure'):
            cls.configure = _patch_configure(cls, cls.configure)

    # ── 3. patch tkinter .config() ──
    _orig_tk_label_config = tk.Label.config
    _orig_tk_button_config = tk.Button.config
    _orig_tk_check_config = tk.Checkbutton.config
    def _tk_config_wrapper(orig):
        def _wrapped(self, **kwargs):
            if 'text' in kwargs:
                kwargs['text'] = _tr(kwargs['text'])
            return orig(self, **kwargs)
        return _wrapped
    tk.Label.config = _tk_config_wrapper(_orig_tk_label_config)
    tk.Button.config = _tk_config_wrapper(_orig_tk_button_config)
    tk.Checkbutton.config = _tk_config_wrapper(_orig_tk_check_config)

    # ── 4. patch StringVar.set() ── 注意：不翻译枚举值，只翻译已知UI文本
    # (移除 StringVar patch，枚举值如 Epoch/Never/Minutes 不能翻译)

from train_ui import main
main()
