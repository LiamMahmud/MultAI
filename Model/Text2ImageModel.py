from diffusers import DiffusionPipeline
import torch


class Text2ImageModel:
    def __init__(self, model_name: str,
                 device: str,
                 **kwargs):
        self.model_name = model_name
        self.model = None
        self.model_path = f'./ModelFiles/Images/{model_name}'
        self.device = device

    def initialize_model(self):
        self.model = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                       torch_dtype=torch.float16,
                                                       use_safetensors=True, variant="fp16")
        self.model.to(self.device)

    def inference(self, prompt: str,
                  n: int = 1,
                  **kwargs):
        for e in range(n):
            image = self.model(prompt=prompt).images[0]
            image.save(f"./media/ImagesMedia/outputImage{e}.jpg")
        return True
