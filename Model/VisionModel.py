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
                  messages: dict,
                  image_file: str = None,
                  max_tokens: int = 350,
                  **kwargs):
        self.validate_prompt(messages)
        messages = self.normalize_to_template(messages)
        if image_file is not None:
            raw_image = Image.open(f"./media/VisionMedia/{image_file}")
            inputs = self.processor(messages, raw_image, return_tensors='pt').to(self.device, torch.float16)
            output = self.model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False)
            decode = self.processor.decode(output[0][0:], skip_special_tokens=True)
        else:
            inputs = self.processor(messages, torch.zeros(1, 3, 224, 224), return_tensors='pt').to(self.device, torch.float16)
            output = self.model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False)
            decode = self.processor.decode(output[0][0:], skip_special_tokens=True)

        return {"role": "assistant", "content": decode.split(" ASSISTANT: ")[-1]}

    @staticmethod
    def validate_prompt(messages):
        valid_roles = {"user", "assistant"}
        for message in messages:
            if "role" not in message or "content" not in message:
                raise ValueError('Invalid format, json must contain "role" and "content" keys.')

            if message["role"] not in valid_roles:
                raise ValueError(f'Invalid role: {message["role"]}. Valid roles are: {valid_roles}')

            if not isinstance(message["content"], str):
                raise ValueError(f'Invalid content type: content must be a string, got {type(message["content"])}.')

    @staticmethod
    def normalize_to_template(messages):
        output = ""
        try:
            for index, message in enumerate(messages):
                if index == 0:
                    output += f"USER: <image>\n{message['content']} "
                else:
                    if message["role"].upper() == "USER":
                        output += f"USER: {message['content']} "
                    if message["role"].upper() == "ASSISTANT":
                        output += f"ASSISTANT: {message['content']}</s>"
            output += "ASSISTANT:"
            return output
        except:
            raise ValueError("Message not formatted properly, must be json with content and role")
    def get_model_path(self):
        if not os.path.exists(self.model_folder_path):
            raise FileExistsError('There is no Model Folder for this defined model in ModelFiles.')
        return self.model_folder_path
