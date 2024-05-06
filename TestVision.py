import base64
from mimetypes import guess_type

import requests



prompts = [
    {"role": "user", "content": "What do you see on this image"},
    {'role': 'assistant', 'content':  'There seems to be 2 cats resting on a sofa'},
    {"role": "user", "content": "What color is the sofa?"}
]
# Example usage:
url = 'http://127.0.0.1:5000/vision'
image_to_upload = 'cats.jpg'
save_path = 'downloaded_image.jpg'

with open(image_to_upload, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
data = {
    "model_name": "Llava_4bit",
    'prompt': prompts,
    "image": encoded_string,  # Including the encoded image directly in the JSON
    "mime_type": "jpg"
}

with open(image_to_upload, 'rb') as f:
    files = {'file': (image_to_upload, f)}
    response = requests.post(url, json=data)

# Upload an image

print(response)
print(response.json())
# with open(save_path, 'wb') as f:
#     f.write(response.content)

# template = f"USER: <image>\n{prompts[0]['content']}\nASSISTANT:"
# text = ""
#
# for index, message in enumerate(prompts):
#     if index == 0:
#         text += f"USER: <image>\n{prompts[index]['content']} "
#     else:
#         if message["role"].upper() == "USER":
#             text += f"USER: {prompts[index]['content']} "
#         if message["role"].upper() == "ASSISTANT":
#             text += f"ASSISTANT: {message['content']}</s>"
# text += "ASSISTANT:"
# print(text)
