from util.import_util import script_imports

script_imports()

# ── ROCm 兼容：全局替换 torch._int_mm 和 torch._scaled_mm ──
import torch, os
if hasattr(torch.version, 'hip') or torch.cuda.is_available():
    _orig_int_mm = getattr(torch, '_int_mm', None)
    _orig_scaled_mm = getattr(torch, '_scaled_mm', None)
    def _safe_int_mm(a, b):
        try:
            return _orig_int_mm(a, b)
        except Exception:
            return torch.mm(a.float(), b.float()).to(a.dtype)
    def _safe_scaled_mm(a, b, **kwargs):
        try:
            return _orig_scaled_mm(a, b, **kwargs)
        except Exception:
            return torch.mm(a.float(), b.float()).to(a.dtype)
    if _orig_int_mm:
        torch._int_mm = _safe_int_mm
    if _orig_scaled_mm:
        torch._scaled_mm = _safe_scaled_mm

from modules.ui.TrainUI import TrainUI


def main():
    ui = TrainUI()
    ui.mainloop()


if __name__ == '__main__':
    main()
