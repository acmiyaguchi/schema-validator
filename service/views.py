from flask import request, jsonify, url_for

from . import app
from .tasks import add


@app.route('/')
def hello_world():
    return 'hello, world'


@app.route('/test_task', methods=['POST'])
def test_task():
    a = request.args['a']
    b = request.args['b']
    task = add.delay(a, b)
    return jsonify({}), 202, {'Location': url_for('task_status',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def test_status(task_id):
    task = add.AsyncResult(task_id)

    response = {"state": task.state}
    if task.state == 'PENDING':
        pass
    elif task.state != 'FAILURE':
        response['result'] = str(task.info)
    else:
        response['result'] = str(task.info)
    return jsonify(response)


@app.route('/__version__')
def version():
    return "OK", 200


@app.route('/__heartbeat__')
def heartbeat():
    return "OK", 200


@app.route('/__lbheartbeat__')
def lbheartbeat():
    return "OK", 200
