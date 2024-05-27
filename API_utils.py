import base64
import os
from io import BytesIO
import urllib.request
import requests
from PIL import Image
from flask import request

UPLOAD_FOLDER = './media'


def stream_output(generator):
    try:
        for token in generator:
            if "content" in token['choices'][0]['delta']:
                content = token['choices'][0]['delta']['content']
                yield content
    except Exception:
        pass


def allowed_audio_file(filename):
    ALLOWED_EXTENSIONS = ["flac", "mp3", "mp4", "mpeg", "mpga", "m4a", "ogg", "wav", "webm"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image_file(filename):
    ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_integer(model_config, values, val_type):
    for e in values:
        if e in model_config:
            model_config[e] = int(model_config[e]) if val_type == "int" else float(model_config[e])
    return model_config


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
                model_config["priority"] = int(model_config["priority"])
                return 200, model_config
        if task.lower() == "speech":
            model_config = request.form.to_dict()
            if "model_name" not in model_config or "prompt" not in model_config:
                return 400, "model_name and prompt are necessary keys"
            if not os.path.isdir(f'./ModelFiles/Audio/{model_config["model_name"]}'):
                return 400, "The model does not exist in the server"

            model_config["model_type"] = "audio"
            model_config["task"] = "speech"
            if "priority" not in model_config:
                model_config["priority"] = 1
            model_config["priority"] = int(model_config["priority"])

            return 200, model_config
    except Exception as e:
        return 400, e
    return 400, "Incorrect endpoint"


def validate_chat_request():
    model_config = request.get_json()
    model_config["model_name"] = model_config["model"]
    # if "model_name" not in model_config:
    #     return 400, "Model needs to be picked"
    if "messages" not in model_config:
        return 400, "No messages sent"
    if not os.path.isdir(f'./ModelFiles/Chat/{model_config["model_name"]}'):
        return 400, "The model does not exist in the server"
    if "priority" not in model_config:
        model_config["priority"] = 1
    model_config = convert_to_integer(model_config, ["n_gpu_layers", "n_threads", "temperature", "max_tokens", "top_k"],
                                      "int")
    model_config = convert_to_integer(model_config,
                                      ["top_p", "presence_penalty", "frequency_penalty", "repeat_penalty"], "float")
    model_config["model_type"] = "chat"

    return 200, model_config


def validate_vision_request():
    try:
        model_config = request.get_json()

        if "model_name" not in model_config:
            return 400, "Model needs to be picked"
        if "messages" not in model_config:
            return 400, "No messages sent"

        if not os.path.isdir(f"./ModelFiles/Vision/{model_config['model_name'].replace('_4bit', '')}"):
            return 400, "The model does not exist in the server"
        if "image" in model_config:

            filename = f'InputVisionImage.{model_config["mime_type"]}'
            model_config["image_file"] = filename
            if type(model_config["image"]) == str and (model_config["image"].startswith("http:/") or model_config["image"].startswith("https:/")):
                urllib.request.urlretrieve(model_config["image"], os.path.join(UPLOAD_FOLDER + "/VisionMedia", filename))

            else:
                image = Image.open(BytesIO(base64.b64decode(model_config["image"])))
                image.save(os.path.join(UPLOAD_FOLDER + "/VisionMedia", filename))

        model_config["model_type"] = "vision"
        if "priority" not in model_config:
            model_config["priority"] = 1
        if "max_tokens" in model_config:
            model_config["max_tokens"] = int(model_config["max_tokens"])
        model_config.pop("image", None)
        return 200, model_config

    except Exception as e:
        print(e)
        return 400, "Invalid request"


def validate_image_request():
    try:
        model_config = request.get_json()
        if "model_name" not in model_config or "prompt" not in model_config:
            return 400, "model_name and prompt are necessary keys"
        if not os.path.isdir(f'./ModelFiles/Images/{model_config["model_name"]}'):
            return 400, "The model does not exist in the server"

        model_config["model_type"] = "images"
        if "priority" not in model_config:
            model_config["priority"] = 1
        if "n" not in model_config:
            model_config["n"] = 1

        if model_config["n"] > 5 or model_config["n"] == 0:
            return 400, "Number of generated images must be between 1 and 5"
        return 200, model_config

    except Exception as e:
        return 400, e


def remove_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
