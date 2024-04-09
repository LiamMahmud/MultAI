import time
from QueueHandler.QueueHandler import Handler
from flask import Flask, request, jsonify, Response, stream_with_context, abort
from api_error_handler import internal_server_error, bad_request
from MemoryHandler.MemoryHandler import MemoryHandler
from chat_endpoint_utils import stream_output, validate_audio_request
from werkzeug.utils import secure_filename
from waitress import serve
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def inference(model):
    return (f"this is {model} inference")


# TODO Intentar pasar stream_output a chat_utils (quizás haciendo que tanto api como utils dependan de queue)


@app.route('/chat/completions', methods=['POST'])
def chat():
    # If the file exists and it is allowed
    try:

        model_config = request.get_json()

        if "model_name" not in model_config or "prompt" not in model_config:
            return bad_request("model_name and prompt are necessary keys")

        model_config["model_type"] = "chat"

        req = queue_handler.add_request(model_config)

        queue_handler.update_queue()

        output = queue_handler.resolve_request(req)
        # print(output)

        if "stream" in model_config and model_config["stream"] == True:
            return Response(stream_with_context(stream_output(queue_handler, output, req)), mimetype='text/plain')

        # return jsonify({'message': 'File uploaded successfully', 'string': output['choices'][0]['message']})
        output["choices"][0]["message"]["content"] = output["choices"][0]["message"]["content"].strip()
        queue_handler.remove_request(req)


        return jsonify(output)
    except Exception as e:
        return internal_server_error(e)

# TODO fix files overwriting when same name
@app.route('/audio/<task>', methods=['POST'])
def audio(task):
    # try:
    model_config = validate_audio_request(task)
    model_config["task"] = "transcribe" if task == "transcriptions" else "translate"

    req = queue_handler.add_request(model_config)
    queue_handler.update_queue()
    output = queue_handler.resolve_request(req)
    queue_handler.remove_request(req)
    os.remove(f"./uploads/{model_config['filename']}")

    return jsonify(output)
    # except Exception as e:
    #     return e
        # return bad_request(str(e))





if __name__ == '__main__':
    memory_handler = MemoryHandler()
    queue_handler = Handler(memory_handler)
    app.run(debug=True)

# serve(app, host='0.0.0.0', port=8080)


# @app.route('/image', methods=['POST'])
# def upload():
#     # Check if the POST request has the file part
#     if 'image' not in request.files:
#         return jsonify({'error': 'No file part'})
#
#     file = request.files['image']
#
#     # If the user does not select a file, the browser submits an empty file without a filename
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})
#
#     # If the file exists and it is allowed
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#         # Get the string data from the POST request
#         string_data = request.form.get('text')
#
#         # Return a JSON response
#         return jsonify({'message': 'File uploaded successfully', 'filename': filename, 'string': string_data})
#
#     return jsonify({'error': 'Invalid file'})


# Function to check if the file extension is allowed


# app.run(debug=True)
