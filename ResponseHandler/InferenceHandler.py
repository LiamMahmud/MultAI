import torch.cuda

from Model.Text2TextModel import Text2TextModel
from Model.VisionModel import VisionModel
from ResponseHandler.MemoryHandler import MemoryHandler
from Model.Speech2TextModel import Speech2TextModel
from Model.Text2SpeechModel import Text2SpeechModel


class InferenceHandler:
    def __init__(self):
        self.current_model_name = None
        self.model = None

    def load_model(self, model_config):
        if model_config["model_type"] == "chat" and model_config["model_name"] != self.current_model_name:
            self.model = Text2TextModel(**model_config)
            self.model.initialize_model()
            self.current_model_name = model_config["model_name"]

        if model_config["model_type"] == "audio" and model_config["model_name"] != self.current_model_name:
            if model_config["task"] == "transcribe" or model_config["task"] == "translate":
                self.model = Speech2TextModel(**model_config)
            else:
                self.model = Text2SpeechModel(**model_config)
            self.model.initialize_model()
            self.current_model_name = model_config["model_name"]

        if model_config["model_type"] == "vision" and model_config["model_name"] != self.current_model_name:
            if self.model is not None and self.model.use_4_bit != model_config["use_4_bit"]:
                self.model = None
                torch.cuda.empty_cache()
            self.model = VisionModel(**model_config)
            self.model.initialize_model()
            self.current_model_name = model_config["model_name"]

    def inference(self, model_config):
        memory_handler = MemoryHandler(model_config)
        if model_config["model_name"] != self.current_model_name:
            self.model = None
            torch.cuda.empty_cache()
        model_config = memory_handler.prepare_memory_configs()
        try:
            self.load_model(model_config)

            output = self.model.inference(**model_config)
            return 200, output
        except Exception as e:
            return 400, str(e)
