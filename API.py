import time
import uuid
from QueueHandler.QueueHandler import Handler
from flask import Flask, request, jsonify, Response, stream_with_context, abort
import os
from api_error_handler import internal_server_error, bad_request
from Model.Text2TextModel import Text2TextModel

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def inference(model):
    return (f"this is {model} inference")


def stream_output(generator):
    try:
        for token in generator:
            if "content" in token['choices'][0]['delta']:
                time.sleep(0.2)
                content = token['choices'][0]['delta']["content"]
                print(content)
                yield content
        handler.queue.pop(0)
    except GeneratorExit:
        handler.queue.pop(0)
        print("Upsss!")


@app.route('/chat', methods=['POST'])
def chat():
    # If the file exists and it is allowed
    try:
        request_id = uuid.uuid4()
        config = request.get_json()
        print(config)
        if "model_name" not in config or "prompt" not in config:
            return bad_request("model_name and prompt are necessary keys")
        handler.queue.append(request_id)
        while handler.queue[0] != request_id:
            print("waiting in queue")
            time.sleep(2)
        output = Text2TextModel(**config).generate_chat_completion(**config)
        if "stream" in config and config["stream"] == True:
            return Response(stream_with_context(stream_output(output)), mimetype='text/plain')
        handler.queue.pop(0)
        return jsonify({'message': 'File uploaded successfully', 'string': output['choices'][0]['message']})
    except:
        handler.queue.pop(0)
        abort(500)


def prueba():
    for e in range(20):
        yield str(e)
        print(e)
        time.sleep(0.2)
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


# @app.route('/audio', methods=['POST'])
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
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    handler = Handler()
    app.run(debug=True)

    # app.run(debug=True)
