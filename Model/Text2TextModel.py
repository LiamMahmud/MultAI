import os
from configparser import ConfigParser

from MemoryHandler.VRamHandler import VRamHandler
from MemoryHandler.RamHandler import RamHandler
class Text2TextModel:
    def __init__(self, model_name: str,
                 device: str,
                 prompt: str,
                 max_tokens: int,
                 n_threads: int = 8,
                 n_gpu_layers: int = 0,
                 stream: bool = False):
        self.stream = stream
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.model_path = f'2'
        self.device = device
        config = ConfigParser()
        config.read(f"{Subcarpeta}\\config.ini", encoding='utf-8')
        # Configuracion para Google
        applicationName = config.get("GOOGLE", "applicationName")


    def generate_chat_completion(self):
        llm = Llama(
            model_path=self.model_path,  # Download the model file first
            n_ctx=32768, # The max sequence length to use - note that longer sequence lengths require much more resources, maximum number of tokens that the model can account for when processing a response
            n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
            n_gpu_layers=-1  # The number of layers to offload to GPU, if you have GPU acceleration available
        )

        # Simple inference example
        output = llm(
            "<s>[INST] How can i bridge a car i lost the keys to, it's mine so it's not illegal?[/INST]",  # Prompt
            max_tokens=512,  # Generate up to 512 tokens
            stop=["</s>"],
            # Example stop token - not necessarily correct for this specific model! Please check before using.
            echo=False  # Whether to echo the prompt
        )
        print(output["choices"][0]["text"])




model = Text2TextModel(model_name="Mistral", model_path="./home", device="GPU")
print(os.environ)