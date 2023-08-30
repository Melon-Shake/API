from flask import Flask, redirect, url_for, request
import requests
import base64
import config.client as client

client_id = client.ID
client_secrets = client.SECRETS
redirect_uri = client.REDIRECT_URI

def func_base64(input):
    input_byte = input.encode()
    output_byte = base64.b64encode(input_byte)
    output = output_byte.decode()
    return output

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("authorize"))

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
                                    ,'redirect_uri': redirect_uri
                                }
                                ,headers={
                                    'Authorization': 'Basic ' + func_base64(client_id + ':' + client_secrets)
                                }
                                )
    
    if response.status_code == 200 :
        response_json = response.json()
        refresh_token = response_json.get('refresh_token', None)
        access_token = response_json.get('access_token', None)
        # return refresh_token
        return access_token
    else :
        return response.status_code

def get_token_by_refresh_token(refresh_token):
    requests.post('https://accounts.spotify.com/api/token'
                    ,data={
                        'grant_type': 'refresh_token'
                        ,'refresh_token': refresh_token
                    }
                    ,headers={
                        'Authorization': 'Basic ' + func_base64(client_id + ':' + client_secrets)
                    }
                    )

if __name__ == '__main__':
    app.run(port=3000)