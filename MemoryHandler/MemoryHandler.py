from configparser import ConfigParser

import torch.cuda

from Model.Text2TextModel import Text2TextModel
from MemoryHandler.MemoryUtils import get_available_VRAM, get_available_RAM, optimal_offload, raise_memory_error
from Model.Speech2TextModel import Speech2TextModel
from Model.Text2SpeechModel import Text2SpeechModel


class MemoryHandler:
    def __init__(self):
        self.current_model_name = None
        self.model = None

    def prepare_memory_configs(self, model_config):
        needed_RAM, needed_VRAM, opt_offload = self.needed_space(model_config)
        model_config["device"] = "cuda"
        if needed_RAM > get_available_RAM():
            raise_memory_error("Not enough RAM, this model cannot be used in this device")
        if needed_VRAM > get_available_VRAM():
            model_config["n_gpu_layers"] = opt_offload
            model_config["device"] = "cpu"
        return model_config

    def needed_space(self, model_config):
        if model_config["model_type"] == "chat":
            config = ConfigParser()
            config.read(f"./ModelFiles/Chat/{model_config['model_name']}/{model_config['model_name']}.ini",
                        encoding='utf-8')
            number_layers = int(config.get("MODEL CONFIG", "number_layers"))
            model_size = float(config.get("MODEL CONFIG", "model_size"))
            opt_offload = optimal_offload(model_size, number_layers) * model_size / number_layers

            if "n_gpu_layers" in model_config:
                offload_layers = model_config["n_gpu_layers"]
                if offload_layers == -1:
                    offload_layers = number_layers
                needed_VRAM = offload_layers * model_size / number_layers
                return [model_size, needed_VRAM, opt_offload]
            else:
                needed_VRAM = model_size
            return [model_size, needed_VRAM, opt_offload]
        if model_config["model_type"] == "audio":
            if model_config["task"] == "transcribe" or model_config["task"] == "translate":
                config = ConfigParser()
                config.read(f"./ModelFiles/Audio/Whisper/Whisper.ini", encoding='utf-8')
                model_size = int(config.get("MODEL CONFIG", model_config["model_name"]))
                return [model_size, model_size, False]
            if model_config["task"] == "speech":
                config = ConfigParser()
                config.read(f'./ModelFiles/Audio/{model_config["model_name"]}/{model_config["model_name"]}.ini',
                            encoding='utf-8')
                model_size = int(config.get("MODEL CONFIG", "model_size"))
                return [model_size, model_size, False]

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
                self.model = Speech2TextModel(**model_config)
            else:
                self.model = Text2SpeechModel(**model_config)
            self.model.initialize_model()
            self.current_model_name = model_config["model_name"]

        if model_config["model_type"] == "image":
            pass

    def inference(self, model_config):
        model_config = self.prepare_memory_configs(model_config)
        print(model_config)
        try:
            self.load_model(model_config)

            output = self.model.inference(**model_config)
            return output
        except:
            raise "Error trying to do Inference, check configuration"
