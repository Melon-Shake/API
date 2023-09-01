import requests
import config.info as info
import base64
import module
client_id = info.id
client_secret = info.secret


Refresh_token = module.read_RefreshToken_from_file()

url = "https://accounts.spotify.com/api/token"
header = {
    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
    }
data = {
    "grant_type": "refresh_token",
    "refresh_token": Refresh_token 
}

response = requests.post(url,headers=header,data=data)

response_json = response.json()
access_token=response_json["access_token"]
with open("config/AuthToken.txt", "w") as file:
        file.write(access_token)
