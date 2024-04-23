import whisper
from typing import Literal


class Speech2TextModel:
    def __init__(self, filename: str,
                 model_name: str,
                 device: str,
                 **kwargs):
        self.model_name = model_name
        self.model = None
        # self.model_path = f'./ModelFiles/Audio/Whisper/{model_name}.pt'
        self.device = device

    def initialize_model(self):
        self.model = whisper.load_model(self.model_name, device=self.device, download_root="./ModelFiles/Audio/Whisper/")

    def inference(self, filename: str,
                  task: Literal['transcribe', 'transcript'],
                  language=None,
                  initial_prompt=None,
                  temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0,),
                  **kwargs):

        result = self.model.transcribe(f'./media/AudioMedia/{filename}', initial_prompt=initial_prompt,
                                       temperature=temperature, language=language, task=task)

        return result
