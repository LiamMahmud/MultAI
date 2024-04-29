import os

import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration


class VisionModel:

    def __init__(self, model_name: str,
                 device,
                 **kwargs):
        self.model = None
        self.processor = None
        self.model_name = model_name
        self.model_folder_path = f"./ModelFiles/Vision/{model_name.replace('_4bit', '')}"
        self.model_path = self.get_model_path()
        self.device = device
        self.use_4_bit = "_4bit" in self.model_name

    def initialize_model(self):
        if self.device == "cuda" and self.use_4_bit:
            self.model = LlavaForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                # use_flash_attention_2=True,
                load_in_4bit=True
            )
        else:
            self.model = LlavaForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                # use_flash_attention_2=True,
            ).to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_path)

    def inference(self,
                  prompt: str,
                  image_file: str,
                  max_tokens: int = 350,
                  **kwargs):
        template = f"USER: <image>\n{prompt}\nASSISTANT:"
        raw_image = Image.open(f"./media/VisionMedia/{image_file}")
        inputs = self.processor(template, raw_image, return_tensors='pt').to(self.device, torch.float16)
        output = self.model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False)
        return self.processor.decode(output[0][0:], skip_special_tokens=True)

    def get_model_path(self):
        if not os.path.exists(self.model_folder_path):
            raise FileExistsError('There is no Model Folder for this defined model in ModelFiles.')
        return self.model_folder_path
