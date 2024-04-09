import whisper
from typing import Literal


class Speech2Text:
    def __init__(self, filename: str,
                 model_name: str,
                 **kwargs):
        self.file = f"./uploads/{filename}"
        self.model_name = model_name
        self.model = None

    def initialize_model(self):
        self.model = whisper.load_model(self.model_name).to("cuda")

    def inference(self, task: Literal['transcribe', 'transcript'],
                  language=None,
                  initial_prompt=None,
                  temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0,),
                  **kwargs):

        result = self.model.transcribe(self.file, initial_prompt=initial_prompt,
                                       temperature=temperature, language=language, task=task)

        return result
