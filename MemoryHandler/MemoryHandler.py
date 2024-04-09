from configparser import ConfigParser

import torch.cuda

from Model.Text2TextModel import Text2TextModel
from MemoryHandler.MemoryUtils import get_available_VRAM, get_available_RAM
from Model.Speech2Text import Speech2Text
import math


class MemoryHandler:
    def __init__(self):
        self.current_model_name = None
        self.model = None

    def is_model_runnable(self, model_config):
        needed_RAM, needed_VRAM = self.needed_space(model_config)
        if needed_RAM > get_available_RAM():
            return "Not enough RAM, this model cannot be used in this device"
        if needed_VRAM > get_available_VRAM():
            return "Not enough VRAM, reduce number of layers or use CPU"
        return True

    def optimal_offload(self, model_size, number_layers):
        output = get_available_VRAM() * number_layers / model_size
        return math.trunc(output) - 1

    def needed_space(self, model_config):
        if model_config["model_type"] == "chat":
            config = ConfigParser()
            config.read(f"./ModelFiles/{model_config['model_name']}/{model_config['model_name']}.ini", encoding='utf-8')
            number_layers = int(config.get("MODEL CONFIG", "number_layers"))
            model_size = float(config.get("MODEL CONFIG", "model_size"))

            if "n_gpu_layers" in model_config:
                offload_layers = model_config["n_gpu_layers"]
                if offload_layers == -1:
                    offload_layers = number_layers
                needed_VRAM = offload_layers * model_size / number_layers
                return [model_size, needed_VRAM]
            else:
                needed_VRAM = self.optimal_offload(model_size, number_layers) * model_size / number_layers
            return [model_size, needed_VRAM]
        if model_config["model_type"] == "audio":
            return [1, 1]

    def load_model(self, model_config):
        if model_config["model_type"] == "chat" and model_config["model_name"] != self.current_model_name:
            self.model = None
            torch.cuda.empty_cache()
            self.model = Text2TextModel(**model_config)
            self.model.initialize_model()
            self.current_model_name = model_config["model_name"]

        if model_config["model_type"] == "audio" and model_config["model_name"] != self.current_model_name:
            self.model = None
            torch.cuda.empty_cache()
            if model_config["task"] == "transcribe" or model_config["task"] == "translate":
                self.model = Speech2Text(**model_config)
            else:
                self.model = False
            self.model.initialize_model()
            self.current_model_name = model_config["model_name"]

        if model_config["model_type"] == "image":
            pass

    def inference(self, model_config):
        if self.is_model_runnable(model_config):
            print(model_config["model_name"], self.current_model_name)
            self.load_model(model_config)

            output = self.model.inference(**model_config)
            return output
