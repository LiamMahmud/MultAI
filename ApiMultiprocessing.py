import time
from multiprocessing import Manager, Process
from flask import Flask, request, jsonify

app = Flask(__name__)
available_models = ["mixtral", "stable_diffusion"]

# Flask routes
@app.route('/chat/<model_name>', methods=['POST'])
def enqueue(model_name):

    if model_name in available_models:
        return "h"


if __name__ == '__main__':
    app.run(debug=True)
