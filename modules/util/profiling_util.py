import platform

import torch


class TorchMemoryRecorder:
    def __init__(self, filename: str = "memory.pickle", enabled: bool = True):
        self.filename = filename
        # ROCm: memory recording is CUDA-only, disable on Windows/non-Linux
        self.enabled = enabled and platform.system() == 'Linux' and torch.cuda.is_available()

    def __enter__(self):
        if self.enabled:
            try:
                torch.cuda.memory._record_memory_history()
            except Exception:
                self.enabled = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enabled:
            try:
                torch.cuda.memory._dump_snapshot(filename=self.filename)
            except Exception:
                print(f"could not write memory snapshot {self.filename}")
            try:
                torch.cuda.memory._record_memory_history(enabled=None)
            except Exception:
                pass

class TorchProfiler:
    def __init__(self, filename: str, enabled: bool = True):
        self.filename = filename
        self.enabled = enabled
        self.profiler = None

    def __enter__(self):
        if self.enabled:
            try:
                profiler_context = torch.profiler.profile(
                    activities=[
                        torch.profiler.ProfilerActivity.CPU,
                        torch.profiler.ProfilerActivity.CUDA
                    ],
                )
                self.profiler = profiler_context.__enter__()
                return self.profiler
            except Exception:
                self.profiler = None
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.profiler is not None:
            try:
                self.profiler.__exit__(exc_type, exc_val, exc_tb)
            except Exception:
                pass
            try:
                self.profiler.export_chrome_trace(self.filename)
            except Exception:
                print(f"could not write profiler output {self.filename}")
            return ret
        else:
            return False
