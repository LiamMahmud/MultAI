import requests




# Example usage:
url = 'http://127.0.0.1:5000/vision'
image_to_upload = 'cats.jpg'
save_path = 'downloaded_image.jpg'

data = {
    "model_name": "Llava_4bit",
    'prompt': "What do you see on this image?",
}


with open(image_to_upload, 'rb') as f:
    files = {'file': (image_to_upload, f)}
    response = requests.post(url, files=files, data=data)

# Upload an image

print(response)
print(response.json())
# with open(save_path, 'wb') as f:
#     f.write(response.content)
