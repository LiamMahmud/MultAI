import requests
import torch
torch.cuda.empty_cache()

url = "http://127.0.0.1:5000/audio/speech"



string_data = "Diez Hordenes, Dalinar, Roshar"

data = {
    'prompt': "Hola, mi nombre es Lucia, ¿como te llamas?",
    "model_name": "Bark-small",
    "voice_preset": "v2/es_speaker_4"
}

response = requests.post(url, data=data)
print(response)
with open('Tests/downloaded_audio.wav', 'wb') as f:
    f.write(response.content)
# response2 = requests.post(url2, files=files, data=data)
