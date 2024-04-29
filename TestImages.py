import requests
import torch

torch.cuda.empty_cache()

url = "http://127.0.0.1:5000/images/generations"

data = {
    'prompt': "very beautiful very red german shepherd dog with blue eyes realistic",
    "model_name": "sdxl-turbo",
    "n": 1
}

response = requests.post(url, json=data)
print(response)
# with open('Tests/Imagesss.zip', 'wb') as f:
#     f.write(response.content)

with open("Tests/Imagesss.jpg", 'wb') as f:
    f.write(response.content)
