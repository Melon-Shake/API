import requests
import lib.module as module
import streamlit as st

access_token = module.read_AuthToken_from_file()

# curl --request GET \
#   --url 'https://api.spotify.com/v1/search?q=%EC%A2%8B%EC%9D%80%EB%82%A0&type=album%2Cartist%2Ctrack&market=kr' \
#   --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'

input_data = '좋은날'

url = f'https://api.spotify.com/v1/search?q={input_data}&type=album%2Cartist%2Ctrack&market=kr'
header = {
    'Authorization': 'Bearer ' + access_token
}

response = requests.get(url, headers=header)
response_json = response.json()
print(response_json)

