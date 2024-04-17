import os
import time
import uuid

import requests
from PIL import Image
from flask import jsonify, request
from werkzeug.utils import secure_filename
from api_error_handler import bad_request

UPLOAD_FOLDER = './media'


def stream_output(queue_handler, generator, req):
    try:
        for token in generator:
            if "content" in token['choices'][0]['delta']:
                content = token['choices'][0]['delta']["content"]
                yield content
        queue_handler.remove_request(req)
    except GeneratorExit:
        print("Upsss!")


def allowed_audio_file(filename):
    ALLOWED_EXTENSIONS = ["flac", "mp3", "mp4", "mpeg", "mpga", "m4a", "ogg", "wav", "webm"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image_file(filename):
    ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_audio_request(task):
    try:
        if task.lower() == "transcriptions" or task.lower() == "translations":
            if 'file' not in request.files:
                return 400, 'No file part'
            file = request.files['file']
            if file.filename == '':
                return 400, 'No selected file'
            model_config = request.form.to_dict()
            if "model_name" not in model_config:
                return 400, "Model needs to be picked"
            if not allowed_audio_file(file.filename):
                print(file.filename)
                return 400, "Not supported filetype"

            model_config["task"] = "transcribe" if task == "transcriptions" else "translate"
            if file:
                filename = f'InputAudio.{file.filename.split(".")[1]}'
                model_config["filename"] = filename
                file.save(os.path.join(UPLOAD_FOLDER + "/AudioMedia", filename))

                model_config["model_type"] = "audio"
                if "priority" not in model_config:
                    model_config["priority"] = 1
                return 200, model_config
        if task.lower() == "speech":
            model_config = request.form.to_dict()
            if "model_name" not in model_config or "prompt" not in model_config:
                return 400, "model_name and prompt are necessary keys"
            if not os.path.isdir(f'./ModelFiles/Audio/{model_config["model_name"]}'):
                return 400, "The model does not exist in the server"

            model_config["model_type"] = "audio"
            model_config["priority"] = 1
            model_config["task"] = "speech"
            return 200, model_config
    except Exception as e:
        return 400, e
    return 400, "Incorrect endpoint"


def validate_chat_request():
    model_config = request.get_json()
    if "model_name" not in model_config or "prompt" not in model_config:
        return 400, "model_name and prompt are necessary keys"
    if not os.path.isdir(f'./ModelFiles/Chat/{model_config["model_name"]}'):
        return 400, "The model does not exist in the server"

    model_config["model_type"] = "chat"
    model_config["priority"] = 1
    return 200, model_config


def validate_vision_request():
    try:
        if 'file' not in request.files:
            return 400, 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 400, 'No selected file'
        model_config = request.form.to_dict()
        print("------------")
        print(type(model_config["use_4_bit"]))
        print("------------")
        if "model_name" not in model_config:
            return 400, "Model needs to be picked"
        if not allowed_image_file(file.filename):
            print(file.filename)
            return 400, "Not supported filetype"
        if not os.path.isdir(f'./ModelFiles/Vision/{model_config["model_name"]}'):
            return 400, "The model does not exist in the server"
        if file:
            if "use_4_bit" not in model_config or model_config["use_4_bit"] != "False":
                model_config["use_4_bit"] = True
            else:
                model_config["use_4_bit"] = False
            filename = f'InputVisionImage.{file.filename.split(".")[1]}'
            model_config["image_file"] = filename
            if file.filename.startswith("http:/") or file.filename.startswith("https:/"):
                image = Image.open(requests.get(file.filename, stream=True).raw)
                image.save(os.path.join(UPLOAD_FOLDER + "/VisionMedia", filename))
            else:
                file.save(os.path.join(UPLOAD_FOLDER + "/VisionMedia", filename))

            model_config["model_type"] = "vision"
            if "priority" not in model_config:
                model_config["priority"] = 1
            return 200, model_config
    except Exception as e:
        print(e)
        return 400, "Invalid request"
