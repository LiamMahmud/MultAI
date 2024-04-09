import os
import time
import uuid

from flask import jsonify, request
from werkzeug.utils import secure_filename
from api_error_handler import bad_request

UPLOAD_FOLDER = './uploads'


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
            return ValueError("Model needs to be picked")
        if not allowed_audio_file(file.filename):
            return ValueError("Not supported filetype")

        if file:
            reqid = uuid.uuid4()
            filename = secure_filename(filename = secure_filename(file.filename.split(".")[0] + str(reqid)[:8] + "." + file.filename.split(".")[1]))
            model_config["filename"] = filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            model_config["model_type"] = "audio"
            if "priority" not in model_config:
                model_config["priority"] = 1
            return model_config
    if task.lower() == "speech":
        pass
    raise ValueError("Incorrect endpoint")


def validate_chat_request(model_config):
    if "model_name" not in model_config or "prompt" not in model_config:
        return bad_request("model_name and prompt are necessary keys")
