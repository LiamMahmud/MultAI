from Model.Text2TextModel import Text2TextModel
from Model import ChatCompletionRequests



prompt = [
    {"role": "system", "content": "You are a question answering assistant."},
    {"role": "user", "content": "Tell me a number from 1 to 100"},
    {'role': 'assistant', 'content':  'Sure! The answer is... 42!'},
    {"role": "user", "content": "Do you remember what number you said before?"}
]

i = {"model_name": "Mistral-7b", "n_gpu_layers": -1, "n_threads": 14, "main_gpu": 0,
     "prompt": prompt, "temperature": 0.8, "max_tokens": 512, "top_p": 0.95,
     "top_k": 40, "stream": False, "presence_penalty": 0.0, "frequency_penalty": 0.0,
     "repeat_penalty": 1.1, "stop": None
     }
x = Text2TextModel(**i)

output = x.generate_chat_completion(**i)

print(output['choices'][0]['message'])
# for out in output:
#     if "content" in out['choices'][0]['delta']:
#         print(out['choices'][0]['delta']["content"], end='')













# import json
# from flask import jsonify
# import requests
#
# # Specify the file to upload
# file_path = 'Apps/Chatbot/BotFaceSinFondo.png'
#
# # Specify the JSON data
# json_data = {'text': 'try1'}
#
# # Make a POST request to the API endpoint
# url = 'http://localhost:5000/chat'
# files = {'image': open(file_path, 'rb')}
# headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
# response = requests.post(url, data=json_data, files=files)
#
# # Check the response
# if response.status_code == 200:
#     print('File uploaded successfully.')
#     print('Response:', response.json())
# else:
#     print('Error:', response.content)
