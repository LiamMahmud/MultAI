import psutil
import pynvml
import math


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


def optimal_offload(model_size, number_layers):
    output = get_available_VRAM() * number_layers / model_size
    return min(0, math.trunc(output) - 3)


def raise_memory_error(message):
    raise MemoryError(message)
