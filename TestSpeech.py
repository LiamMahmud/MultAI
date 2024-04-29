import requests
import torch
torch.cuda.empty_cache()

url = "http://127.0.0.1:5000/audio/speech"



string_data = "Diez Hordenes, Dalinar, Roshar"

data = {
    'prompt': "Hola, mi nombre es Lucia, ¿como te llamas tu?",
    "model_name": "Bark",
}

response = requests.post(url, data=data)
print(response)
with open('Tests/downloaded_audio.wav', 'wb') as f:
    f.write(response.content)
# response2 = requests.post(url2, files=files, data=data)
