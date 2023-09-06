import requests
import lib.module as module
import streamlit as st
from sp_artist import SpotifyArtistsORM, SpotifyArtistsEntity
from model.database import session_scope

access_token = module.read_AuthToken_from_file()

# curl --request GET \
#   --url 'https://api.spotify.com/v1/search?q=%EC%A2%8B%EC%9D%80%EB%82%A0&type=album%2Cartist%2Ctrack&market=kr' \
#   --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'

input_data = '아이유'

url = f'https://api.spotify.com/v1/search?query={input_data}&type=artist&locale=en-US%2Cen%3Bq%3D0.9&offset=0&limit=20'
header = {
    'Authorization': 'Bearer ' + access_token
}

response = requests.get(url, headers=header)
response_json = response.json()

items = response_json.get('artists', {}).get('items', [])

with session_scope() as session:
    for item in items:
        # 각 필드에 대한 값을 변수에 할당
        external_urls = item.get('external_urls', {}).get('spotify', '')
        genres = ', '.join(item.get('genres', []))
        href = item.get('href', '')
        id = item.get('id', '')
        images_url = item.get('images', [])[0].get('url', '') if item.get('images') else ''
        name = item.get('name', '')
        popularity = item.get('popularity', 0)
        type = item.get('type', '')
        uri = item.get('uri', '')

        # SpotifyArtistsORM 객체 생성
        orm = SpotifyArtistsORM(
            external_urls=external_urls,
            genres=genres,
            href=href,
            id=id,
            images_url=images_url,
            name=name,
            popularity=popularity,
            type=type,
            uri=uri
        )
        session.add(orm)
