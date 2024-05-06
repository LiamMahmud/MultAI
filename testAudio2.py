import requests
import torch

url = "http://127.0.0.1:5000/audio/translations"
url2 = "http://127.0.0.1:5000/audio/transcriptions"

file_path = "Tests/ECDLR.m4a"
file = open(file_path, "rb")

files = {"file": file}

string_data = "Diez Hordenes, Dalinar, Roshar"

data = {
    'prompt': string_data,
    "model_name": "medium"
}

# response = requests.post(url, files=files, data=data)
response2 = requests.post(url2, files=files, data=data)
print(response2.json()["text"])
print(response2.json())
