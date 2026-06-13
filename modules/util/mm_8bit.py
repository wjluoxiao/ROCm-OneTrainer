try:
    from modules.util.triton_mm_8bit import mm_8bit
except ImportError as e:
    print(str(e) + ", continuing without triton")
    import torch, os
    # ROCm: _int_mm and _scaled_mm are CUDA-only, use CPU fallback
    _ROCm = os.environ.get("ROCM_HOME") or torch.cuda.is_available() and hasattr(torch.version, 'hip')
    def mm_8bit(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        assert a.shape[1] == b.shape[0], "Incompatible dimensions"
        assert a.is_contiguous(), "Matrix A must be contiguous"
        assert a.dtype == b.dtype, "Incompatible dtypes"
        assert a.dtype in [torch.int8, torch.float8_e4m3fn]
        if _ROCm:
            # ROCm: use CPU fallback, avoid torch._int_mm segfault
            return torch.mm(a.float(), b.float()).to(a.dtype)
        if a.dtype == torch.int8:
            try:
                return torch._int_mm(a, b)
            except Exception:
                return torch.mm(a.float(), b.float()).to(a.dtype)
        else:
            try:
                one = torch.ones(1, device=a.device)
                return torch._scaled_mm(a, b.T.contiguous().T, scale_a=one, scale_b=one)
            except Exception:
                return torch.mm(a.float(), b.float()).to(a.dtype)
