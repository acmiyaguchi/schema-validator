from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello, world'


@app.route('/__version__')
def version():
    return "OK", 200

@app.route('/__heartbeat__')
def heartbeat():
    return "OK", 200


@app.route('/__lbheartbeat__')
def lbheartbeat():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
