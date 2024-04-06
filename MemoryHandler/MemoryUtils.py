import psutil
import pynvml


def get_available_VRAM():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming the first GPU
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    vram_gb = mem_info.free / (1024 ** 3)  # Convert bytes to GB
    return vram_gb


def get_available_RAM():
    ram_bytes = psutil.virtual_memory().available
    ram_gb = ram_bytes / (1024 ** 3)  # Convert bytes to GB
    return ram_gb


def raise_memory_error(message):
    raise MemoryError(message)
