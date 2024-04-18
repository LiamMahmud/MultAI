import psutil
import pynvml
import math
from configparser import ConfigParser


class MemoryHandler:
    def __init__(self, model_config: dict):
        self.model_config = model_config

    def prepare_memory_configs(self):
        needed_RAM, needed_VRAM, opt_offload = self.needed_space()
        self.model_config["device"] = "cuda"
        if needed_RAM > self.get_available_RAM():
            raise_memory_error("Not enough RAM, this model cannot be used in this device")
        if needed_VRAM > self.get_available_VRAM():
            self.model_config["n_gpu_layers"] = opt_offload
            self.model_config["device"] = "cpu"
        return self.model_config

    def needed_space(self):
        if self.model_config["model_type"] == "chat":
            config_path = f"./ModelFiles/Chat/{self.model_config['model_name']}/{self.model_config['model_name']}.ini"
            number_layers = int(self.read_model_config(config_path, "number_layers"))
            model_size = float(self.read_model_config(config_path, "model_size"))
            opt_offload = self.optimal_offload(model_size, number_layers) * model_size / number_layers

            if "n_gpu_layers" in self.model_config:
                offload_layers = self.model_config["n_gpu_layers"]
                if offload_layers == -1:
                    offload_layers = number_layers
                needed_VRAM = offload_layers * model_size / number_layers
                return [model_size, needed_VRAM, opt_offload]
            else:
                needed_VRAM = model_size
            return [model_size, needed_VRAM, opt_offload]
        if self.model_config["model_type"] == "audio":
            if self.model_config["task"] == "transcribe" or self.model_config["task"] == "translate":
                config_path = f"./ModelFiles/Audio/Whisper/Whisper.ini"
                model_size = int(self.read_model_config(config_path, self.model_config["model_name"]))
                return [model_size, model_size, False]
            if self.model_config["task"] == "speech":
                config_path = f'./ModelFiles/Audio/{self.model_config["model_name"]}/{self.model_config["model_name"]}.ini'
                model_size = int(self.read_model_config(config_path, "model_size"))
                return [model_size, model_size, False]

        if self.model_config["model_type"] == "vision":
            config_path = f"./ModelFiles/Vision/Llava/{self.model_config['model_name'].replace('_4bit', '')}.ini"
            model_size = int(self.read_model_config(config_path, "model_size"))
            model_size_4bit = int(self.read_model_config(config_path, "model_size_4bit"))
            if "use_4_bit" in self.model_config["model_name"]:
                return [model_size, model_size_4bit, False]
            return [model_size, model_size, False]
        raise "Wrong model configuration"

    def optimal_offload(self, model_size, number_layers):
        output = self.get_available_VRAM() * number_layers / model_size
        return min(0, math.trunc(output) - 3)

    @staticmethod
    def read_model_config(path, attribute):
        config = ConfigParser()
        config.read(path, encoding='utf-8')

        output = config.get("MODEL CONFIG", attribute)
        return output

    @staticmethod
    def get_available_VRAM():
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming the first GPU
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            vram_gb = mem_info.free / (1024 ** 3)  # Convert bytes to GB
        except:
            vram_gb = 0
        return vram_gb

    @staticmethod
    def get_available_RAM():
        ram_bytes = psutil.virtual_memory().available
        ram_gb = ram_bytes / (1024 ** 3)  # Convert bytes to GB
        return ram_gb


def raise_memory_error(message):
    raise MemoryError(message)
