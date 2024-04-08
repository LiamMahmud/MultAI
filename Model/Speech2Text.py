import whisper


class Speech2Text:
    def __init__(self, filename: str,
                 model_name: str,
                 **kwargs):
        self.file = f"./uploads/{filename}"
        self.model_name = model_name
        self.model = None

    def initialize_model(self):
        print(self.model_name)
        self.model = whisper.load_model(self.model_name)

    def inference(self, language = None,
                  prompt=None,
                  temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
                  **kwargs):
        result = self.model.transcribe(self.file, initial_prompt=prompt,
                                       temperature=temperature)
        print(result["text"])
        return result

# data = {
#     'text': "Roshar",
#     "model_name": "medium"
# }
# x = Speech2Text(**data)
