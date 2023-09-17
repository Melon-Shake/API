import requests
import lib.module as module

access_token = module.read_AuthToken_from_file()

input_data = '좋은날'

url = f'https://api.spotify.com/v1/search?q={input_data}&type=album%2Cartist%2Ctrack&market=kr'
header = {
    'Authorization': 'Bearer ' + access_token
}

response = requests.get(url, headers=header)
response_json = response.json()
print(response_json)

