from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("authorize"),code=302)

@app.route("/authorize")
def authorize():
    response = "hello"
    return response

if __name__ == '__main__':
    app.run(port=3000)