import os
import time
import uuid

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


def validate_audio_request(task):
    if task.lower() == "transcriptions" or task.lower() == "translations":
        if 'file' not in request.files:
            raise ValueError('No file part')
        file = request.files['file']
        if file.filename == '':
            raise ValueError('No selected file')
        model_config = request.form.to_dict()
        if "model_name" not in model_config:
            raise ValueError("Model needs to be picked")
        if not allowed_audio_file(file.filename):
            raise ValueError("Not supported filetype")
        model_config["task"] = "transcribe" if task == "transcriptions" else "translate"
        if file:
            filename = f'InputAudio.{file.filename.split(".")[1]}'
            model_config["filename"] = filename
            file.save(os.path.join(UPLOAD_FOLDER + "/AudioInputs", filename))

            model_config["model_type"] = "audio"
            if "priority" not in model_config:
                model_config["priority"] = 1
            return model_config
    if task.lower() == "speech":
        model_config = request.form.to_dict()
        if "model_name" not in model_config or "prompt" not in model_config:
            raise ValueError("model_name and prompt are necessary keys")

        model_config["model_type"] = "audio"
        model_config["priority"] = 1
        model_config["task"] = "speech"
        return model_config

    raise ValueError("Incorrect endpoint")


def validate_chat_request():
    model_config = request.get_json()
    if "model_name" not in model_config or "prompt" not in model_config:
        raise ValueError("model_name and prompt are necessary keys")

    model_config["model_type"] = "chat"
    model_config["priority"] = 1
    return model_config
