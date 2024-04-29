import torch
from diffusers import AutoPipelineForText2Image


class Text2ImageModel:
    def __init__(self, model_name: str,
                 device: str,
                 **kwargs):
        self.model_name = model_name
        self.model = None
        self.model_path = f'./ModelFiles/Images/{model_name}'
        self.device = device

    def initialize_model(self):
        self.model = AutoPipelineForText2Image.from_pretrained(self.model_path, torch_dtype=torch.float16, variant="fp16")
        self.model.to(self.device)

    def inference(self, prompt: str,
                  n: int,
                  number_steps: int = 4,
                  **kwargs):
        for e in range(n):
            image = self.model(prompt=prompt, num_inference_steps=number_steps, guidance_scale=0.0).images[0]
            image.save(f"./media/ImagesMedia/outputImage{e}.jpg")
        return True
