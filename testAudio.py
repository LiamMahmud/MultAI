import requests


url = "http://127.0.0.1:5000/audio/transcript"

file_path = "./ECDLR.m4a"
file = open(file_path, "rb")

files = {"file": file}

string_data = "Diez Hordenes, Dalinar, Roshar"

data = {
    'prompt': string_data,
    "model_name": "large"
}

response = requests.post(url, files=files, data=data)
print(response.json()["text"])
