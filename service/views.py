import json

from flask import request, jsonify, url_for

from . import app
from .tasks import spark_submit


@app.route('/')
def hello_world():
    return 'hello, world'


@app.route('/submit', methods=['POST'])
def submit():
    schema_id = request.args.get('schema_id')
    dataset_id = request.args.get('dataset_id')
    task = spark_submit.delay(schema_id, dataset_id)
    return (
        jsonify({'task_id': task.id}),
        202,
        {'Location': url_for('task_status', task_id=task.id)}
    )


@app.route('/status/<task_id>')
def task_status(task_id):
    task = spark_submit.AsyncResult(task_id)

    response = {"state": task.state}
    if task.state == 'PENDING':
        pass
    elif task.state != 'FAILURE':
        response['result'] = json.loads(task.info)
    else:
        response['result'] = json.loads(task.info)
    return jsonify(response)


@app.route('/__version__')
def version():
    # TODO: add a version object to the project
    return "OK", 200


@app.route('/__heartbeat__')
def heartbeat():
    return "OK", 200


@app.route('/__lbheartbeat__')
def lbheartbeat():
    return "OK", 200
