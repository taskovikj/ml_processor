import celery.states as states
from flask import Flask, Response
from flask import url_for, jsonify
from worker import celery
from flask import Flask, jsonify, request



dev_mode = True
app = Flask(__name__)


@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json['data']

    result = data.upper()

    return jsonify(result), 200


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


@app.route('/enqueue-ml-task')
def enqueue_ml_task():
    data = "Some data for the ML task"
    from celery_queue.tasks import run_ml_task
    result = run_ml_task.apply_async(args=[data], queue='ml_queue')
    return f"ML Task enqueued: {result.id}"
