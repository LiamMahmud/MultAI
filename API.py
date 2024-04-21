import os
from flask import Flask, request, jsonify, Response, stream_with_context, send_file, after_this_request
from ResponseHandler.InferenceHandler import InferenceHandler
from QueueHandler.QueueHandler import Handler
from api_error_handler import internal_server_error, bad_request
from chat_endpoint_utils import stream_output, validate_audio_request, validate_chat_request, validate_vision_request

app = Flask(__name__)

UPLOAD_FOLDER = './media'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def inference(model):
    return (f"this is {model} inference")


# TODO Intentar pasar stream_output a chat_utils (quizás haciendo que tanto api como utils dependan de queue)


@app.route('/chat/completions', methods=['POST'])
def chat():
    # If the file exists and it is allowed
    print("HELLO")
    code, model_config = validate_chat_request()
    if code != 200:
        return bad_request(str(model_config))

    req = queue_handler.add_request(model_config)

    queue_handler.update_queue()

    code, output = queue_handler.resolve_request(req)
    if code != 200:
        return bad_request(str(output))
    # print(output)
    print(output)
    if "stream" in model_config and model_config["stream"] == True:
        return Response(stream_with_context(stream_output(queue_handler, output, req)), mimetype='text/plain')

    # return jsonify({'message': 'File uploaded successfully', 'string': output['choices'][0]['message']})
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

    print(model_config)
    req = queue_handler.add_request(model_config)
    print(req)
    # try:
    queue_handler.update_queue()
    code, output = queue_handler.resolve_request(req)
    if code != 200:
        return bad_request(str(output))
    return jsonify(output)
    # except Exception as e:
    #     print(e)
    #     return bad_request(str(e))


if __name__ == '__main__':
    memory_handler = InferenceHandler()
    queue_handler = Handler(memory_handler)
    app.run(host='0.0.0.0', port=5000)

# serve(app, host='0.0.0.0', port=8080)

# TODO do validation of input config,
# Auto voice preset for Text2Speech
# try and fix load model not using chec of same model in vision



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
