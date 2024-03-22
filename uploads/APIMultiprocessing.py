from flask import Flask, jsonify
from celery import Celery

app = Flask(__name__)
celery = Celery(app.name, broker='redis://localhost:6379/0')

@celery.task
def process_task(data):
    # Simulate processing
    print("Processing task:", data)

@app.route('/enqueue_task/<data>')
def enqueue_task(data):
    process_task.delay(data)
    return jsonify({'message': 'Task enqueued successfully'})

if __name__ == '__main__':
    app.run(debug=True)
