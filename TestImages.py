import requests
import torch

torch.cuda.empty_cache()

url = "http://127.0.0.1:5000/images/generations"

data = {
    'prompt': "A beautiful lion jumping from a very red and big rock",
    "model_name": "Stable-Diffusion-xl",
}

response = requests.post(url, json=data)
print(response)
with open('Tests/lion.jpg', 'wb') as f:
    f.write(response.content)
