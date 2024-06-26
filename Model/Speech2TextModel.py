import whisper
from typing import Literal


class Speech2TextModel:
    def __init__(self, model_name: str,
                 device: str,
                 **kwargs):
        self.model_name = model_name
        self.model = None
        self.device = device

    def initialize_model(self):
        self.model = whisper.load_model(self.model_name, device=self.device, download_root="./ModelFiles/Audio/Whisper/")

    def inference(self, filename: str,
                  task: Literal['transcribe', 'transcript'],
                  language: str = None,
                  initial_prompt: str = None,
                  **kwargs):

        result = self.model.transcribe(f'./media/AudioMedia/{filename}', initial_prompt=initial_prompt,
                                       language=language, task=task)

        return result
