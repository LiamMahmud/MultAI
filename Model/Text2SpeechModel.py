from transformers import AutoProcessor, BarkModel
import scipy
import io


class Text2SpeechModel:
    def __init__(self, model_name: str,
                 device: str,
                 voice_preset: str = None,
                 **kwargs):
        self.model_name = model_name
        self.model = None
        self.processor = None
        self.voice_preset = voice_preset
        self.model_path = f'./ModelFiles/Audio/{model_name}'
        self.device = device

    def initialize_model(self):
        self.processor = AutoProcessor.from_pretrained(self.model_path)
        self.model = BarkModel.from_pretrained(self.model_path).to(self.device)

    def inference(self, prompt: str,
                  **kwargs):
        inputs = self.processor(prompt, voice_preset=self.voice_preset).to(self.device)

        audio_array = self.model.generate(**inputs)
        audio_array = audio_array.cpu().numpy().squeeze()
        sample_rate = self.model.generation_config.sample_rate
        scipy.io.wavfile.write("./media/AudioMedia/AudioOutput.wav", rate=sample_rate, data=audio_array)

        return [audio_array, sample_rate]
