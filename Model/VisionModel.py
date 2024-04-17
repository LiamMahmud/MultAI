import os
from configparser import ConfigParser

import requests
import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration


class VisionModel:

    def __init__(self, model_name: str,
                 device,
                 use_4_bit: bool = True,
                 **kwargs):
        self.model = None
        self.processor = None
        self.model_name = model_name
        self.model_folder_path = f'./ModelFiles/Vision/{model_name}'
        self.model_path = self.get_model_path()
        self.device = device
        self.use_4_bit = bool(use_4_bit)

    def initialize_model(self):
        print(self.use_4_bit)
        # if self.device == "cuda" and self.use_4_bit == True:
        #     self.model = LlavaForConditionalGeneration.from_pretrained(
        #         self.model_path,
        #         torch_dtype=torch.float16,
        #         low_cpu_mem_usage=True,
        #         # use_flash_attention_2=True,
        #         load_in_4bit=True
        #     )
        # else:
        self.model = LlavaForConditionalGeneration.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            # use_flash_attention_2=True,
            load_in_4bit=self.use_4_bit
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

        return self.processor.decode(output[0][2:], skip_special_tokens=True)

    def get_model_path(self):
        if not os.path.exists(self.model_folder_path):
            raise FileExistsError('There is no Model Folder for this defined model in ModelFiles.')
        return self.model_folder_path
