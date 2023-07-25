from flask import Flask, request, jsonify
from celery import Celery
import time

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6380/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6380/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Celery task function
@celery.task
def process_string_task(input_string):
    # Simulating some processing delay
    time.sleep(5)
    # Your processing logic here (replace this with your actual processing code)
    return input_string.upper()


# Flask route for processing the string
@app.route('/process_string', methods=['POST'])
def process_string():
    data = request.get_json()
    input_string = data['input_string']

    # Send the input_string to Celery for processing asynchronously
    result = process_string_task.delay(input_string)

    return jsonify({'task_id': result.id}), 202  # Return task ID and status 202 Accepted


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
