from flask import Flask, redirect, url_for, request
import requests
import base64
import client

client_id = client.ID
client_secrets = client.SECRETS
redirect_uri = client.REDIRECT_URI

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("authorize"),code=302)

@app.route('/authorize')
def authorize():
    return redirect('https://accounts.spotify.com/authorize?'
                        +f'client_id={client_id}'
                        +f'&redirect_uri={redirect_uri}'
                        +f'&response_type=code'
                        )

@app.route('/callback')
def callback():
    code = request.args.get('code', None)
    response = requests.post('https://accounts.spotify.com/api/token'
                                ,data={
                                    'grant_type': 'authorization_code'
                                    ,'code': code
                                }
                                ,headers={
                                    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secrets).encode()).decode()
                                }
                                )
    
    if response.status_code == 200 :
        print("!!!!!!!!!!!!!!!!!!!!!!!!")
    else :
        print(f'>>>>>>>>>> {response.status_code}')


    return "안녕"

if __name__ == '__main__':
    app.run(port=3000)