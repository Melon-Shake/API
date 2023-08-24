from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hi"

if __name__ == '__main__':
    app.run(port=3000)