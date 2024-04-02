import json
from flask import jsonify
import requests
import time

# Specify the file to upload
file_path = 'Apps/Chatbot/BotFaceSinFondo.png'

# Specify the JSON data
prompt = [
    {"role": "system", "content": "You are a question answering assistant."},
    {"role": "user", "content": "Tell me a number from 1 to 100"},
    {'role': 'assistant', 'content':  'Sure! The answer is... 42!'},
    {"role": "user", "content": "Do you remember what number you said before?"}
]

i = {"model_name": "Mistral-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
     "prompt": prompt, "temperature": 0.1, "max_tokens": 512, "top_p": 0.95,
     "top_k": 40, "stream": True, "presence_penalty": 0.0, "frequency_penalty": 0.0,
     "repeat_penalty": 1.1, "stop": None
     }

# Make a POST request to the API endpoint
url = 'http://localhost:5000/chat'
# files = {'image': open(file_path, 'rb')}
# headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
# start_time = time.time()
# response = requests.post(url, json=i, stream=True)

with requests.post(url, json=i, stream=True) as r:
    for line in r.iter_content():
        print(line.decode("utf-8"), end="")


# print(response.json())
# print("--- %s seconds ---" % (time.time() - start_time))
# Check the response
# if response.status_code == 200:
#     print('Response:', response.json())
# else:
#     print('Error:', response.content)
