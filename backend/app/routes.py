from app import app


@app.route("/", methods=['GET'])
def hello_world():
    return 'Hello World!'
