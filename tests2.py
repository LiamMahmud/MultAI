import json
from flask import jsonify
import requests

# Specify the file to upload
file_path = 'Apps/Chatbot/BotFaceSinFondo.png'

# Specify the JSON data
json_data = {'text': 'try2'}

# Make a POST request to the API endpoint
url = 'http://localhost:5000/chat'
files = {'image': open(file_path, 'rb')}
headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
response = requests.post(url, data=json_data, files=files)

# Check the response
if response.status_code == 200:
    print('File uploaded successfully.')
    print('Response:', response.json())
else:
    print('Error:', response.content)
