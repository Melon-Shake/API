from flask import Flask, redirect, url_for
import client

client_id = client.ID
redirect_uri = client.REDIRECT_URI

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("authorize"),code=302)

@app.route('/authorize')
def authorize():
    response = redirect('https://accounts.spotify.com/authorize?'
                        +f'client_id={client_id}'
                        +f'&redirect_uri={redirect_uri}'
                        +f'&response_type=code'
                        )
    return response

if __name__ == '__main__':
    app.run(port=3000)