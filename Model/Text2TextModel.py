import os
from typing import Optional, Union, List
from configparser import ConfigParser
from llama_cpp import Llama
from Model.ChatCompletionRequests import ChatCompletionRequestMessage


class Text2TextModel:

    def __init__(self, model_name: str,
                 n_threads: Optional[int] = None,
                 n_gpu_layers: int = 0,
                 main_gpu: int = 0,
                 **kwargs):

        self.model = None
        self.model_name = model_name
        self.model_folder_path = f'./ModelFiles/Chat/{model_name}'
        self.model_path = self.get_model_path()
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.main_gpu = main_gpu

        config = ConfigParser()
        config.read(f"{self.model_folder_path}/{self.model_name}.ini", encoding='utf-8')
        self.context_window = int(config.get("MODEL CONFIG", "context_window"))

    def initialize_model(self):
        self.model = Llama(
            model_path=self.model_path,
            n_ctx=self.context_window,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers
        )

    def inference(self,
                  messages: ChatCompletionRequestMessage,
                  temperature: int = 0.2,
                  max_tokens: int = 512,
                  top_p: float = 0.95,
                  top_k: int = 40,
                  stream: bool = False,
                  presence_penalty: float = 0.0,
                  frequency_penalty: float = 0.0,
                  repeat_penalty: float = 1.1,
                  stop: Optional[Union[str, List[str]]] = None,
                  **kwargs):

        self.validate_prompt(messages)
        output = self.model.create_chat_completion(messages=messages,
                                                   model=self.model_name,
                                                   temperature=temperature,
                                                   max_tokens=max_tokens,
                                                   top_p=top_p,
                                                   top_k=top_k,
                                                   stream=stream,
                                                   presence_penalty=presence_penalty,
                                                   frequency_penalty=frequency_penalty,
                                                   repeat_penalty=repeat_penalty,
                                                   stop=stop
                                                   )
        return output

    @staticmethod
    def validate_prompt(messages):
        valid_roles = {"system", "user", "assistant"}
        for message in messages:
            if "role" not in message or "content" not in message:
                raise ValueError('Invalid format, json must contain "role" and "content" keys.')

            if message["role"] not in valid_roles:
                raise ValueError(f'Invalid role: {message["role"]}. Valid roles are: {valid_roles}')

            if not isinstance(message["content"], str):
                raise ValueError(f'Invalid content type: content must be a string, got {type(message["content"])}.')

    def get_model_path(self):
        if not os.path.exists(self.model_folder_path):
            raise FileExistsError('There is no Model Folder for this defined model in ModelFiles.')
        for filename in os.listdir(self.model_folder_path):
            _, ext = os.path.splitext(filename)
            if ext == '.gguf':
                return os.path.join(self.model_folder_path, filename)
        raise FileExistsError('There is not a .gguf file in the model folder.')
