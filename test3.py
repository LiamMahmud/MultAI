import json
from flask import jsonify
import requests
import time


file_path = 'Apps/Chatbot/BotFaceSinFondo.png'

prompt = [
    {"role": "system", "content": "You are a question answering assistant."},
    {"role": "user", "content": "Tell me a number from 1 to 100"},
    {'role': 'assistant', 'content':  'Sure! The answer is... 42!'},
    {"role": "user", "content": "Do you remember what number you said before?"}
]

i = {"model_name": "Llama2-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
     "prompt": prompt, "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
     "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
     "repeat_penalty": 1.1, "stop": None
     }

url = 'http://localhost:5000/chat'

for e,i in enumerate(["sdfsd","aada"]):
    print(e,i)
start_time = time.time()
response = requests.post(url, json=i)
print(response.json()["string"]["content"])
print("Time:", time.time() - start_time)
