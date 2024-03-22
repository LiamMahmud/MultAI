import time
import uuid
from QueueHandler.QueueHandler import Handler
from flask import Flask, request, jsonify
import os


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def inference(model):
    return(f"this is {model} inference")


@app.route('/chat', methods=['POST'])
def chat():
    # If the file exists and it is allowed
    request_id = uuid.uuid4()
    if request.form.get("text"):
        string_data = request.form.get('text')
        handler.queue.append(request_id)
        if request.form.get("text") == "try1":
            time.sleep(10)
            print(handler.queue)
        while handler.queue[0] != request_id:
            print("waiting in queue")
            time.sleep(3)
        handler.queue.pop(0)
        return jsonify({'message': 'File uploaded successfully', 'string': string_data})


    return jsonify({'error': 'Invalid file'})

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
