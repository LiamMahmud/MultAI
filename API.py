import os

import zipstream
from flask import Flask, jsonify, Response, stream_with_context, send_file, after_this_request

from API_utils import stream_output, validate_audio_request, validate_chat_request, validate_vision_request, \
    validate_image_request
from QueueHandler.QueueHandler import Handler
from ResponseHandler.InferenceHandler import InferenceHandler
from api_error_handler import bad_request

app = Flask(__name__)

UPLOAD_FOLDER = './media'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/chat/completions', methods=['POST'])
def chat():
    @after_this_request
    def remove_file(response):
        try:
            queue_handler.remove_request(req)
        finally:
            return response
    # If the file exists and it is allowed
    code, model_config = validate_chat_request()
    if code != 200:
        return bad_request(str(model_config))

    req = queue_handler.add_request(model_config)

    queue_handler.update_queue()

    code, output = queue_handler.resolve_request(req)
    if code != 200:
        return bad_request(str(output))

    if "stream" in model_config and model_config["stream"] == True:
        return Response(stream_with_context(stream_output(queue_handler, output, req)), mimetype='text/plain')

    output["choices"][0]["message"]["content"] = output["choices"][0]["message"]["content"].strip()
    queue_handler.remove_request(req)

    return jsonify(output)


@app.route('/audio/<task>', methods=['POST'])
def audio(task):
    @after_this_request
    def remove_file(response):
        try:
            queue_handler.remove_request(req)
        finally:
            return response

    code, model_config = validate_audio_request(task)
    if code != 200:
        return bad_request(str(model_config))

    req = queue_handler.add_request(model_config)
    queue_handler.update_queue()
    code, output = queue_handler.resolve_request(req)
    if code != 200:
        return bad_request(str(output))

    if task.lower() == "transcriptions" or task.lower() == "translations":
        return jsonify(output)
    else:

        return send_file("./media/AudioMedia/AudioOutput.wav", as_attachment=True)


@app.route('/vision', methods=['POST'])
def vision():
    @after_this_request
    def remove_file(response):
        try:
            queue_handler.remove_request(req)
        finally:
            return response

    code, model_config = validate_vision_request()
    if code != 200:
        return bad_request(str(model_config))

    req = queue_handler.add_request(model_config)
    queue_handler.update_queue()
    code, output = queue_handler.resolve_request(req)
    if code != 200:
        return bad_request(str(output))
    return jsonify(output)



@app.route('/images/generations', methods=['POST'])
def images():
    @after_this_request
    def remove_file(response):
        try:
            queue_handler.remove_request(req)
        finally:
            return response

    code, model_config = validate_image_request()
    if code != 200:
        return bad_request(str(model_config))
    req = queue_handler.add_request(model_config)
    queue_handler.update_queue()
    code, output = queue_handler.resolve_request(req)
    if code != 200:
        return bad_request(str(output))
    if model_config["n"] == 1:
        return send_file("./media/ImagesMedia/outputImage0.jpg", as_attachment=True)
    else:
        zipFile = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        for e in range(model_config["n"]):
            zipFile.write(f'./media/ImagesMedia/outputImage{e}.jpg', arcname=f'outputImage{e}.jpg')

        response = Response(zipFile, mimetype='application/zip')
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format('files.zip')
        return response

@app.route('/list/models', methods=['GET'])
def list_models():
    origin_folder = './ModelFiles'
    models = {}
    # List directories at the first level
    for first_level in os.listdir(origin_folder):
        first_level_path = os.path.join(origin_folder, first_level)
        if os.path.isdir(first_level_path):  # Ensure it's a directory
            models.setdefault(first_level, [])

            # List directories at the second level
            for second_level in os.listdir(first_level_path):
                second_level_path = os.path.join(first_level_path, second_level)
                if os.path.isdir(second_level_path):  # Ensure it's a directory
                    models[first_level].append(second_level)
    return models

if __name__ == '__main__':
    memory_handler = InferenceHandler()
    queue_handler = Handler(memory_handler)
    app.run(host='0.0.0.0', port=5000)

# serve(app, host='0.0.0.0', port=8080)
