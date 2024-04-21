# app.py
# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return "Hello, Docker!"
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)
import requests

url = 'http://127.0.0.1:5000/'

response = requests.get(url)

# Print the response text (the content of the response)
print('Response from Flask App:', response.text)
