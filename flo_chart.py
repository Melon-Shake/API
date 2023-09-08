import json
import re
import sys
from datetime import datetime, timedelta



import requests

_APP_VERSION = ""
_APP_NAME = "FLO"
_USER_AGENT = "okhttp/4.9.2"
_CHART_API_URL = "https://api.music-flo.com/display/v1/browser/chart/1/list?mixYn=N"


class FloChartRequestException(Exception):
    pass

headers = {
    "User-Agent": _USER_AGENT,
    "x-gm-app-name": _APP_NAME,
    "x-gm-app-version": _APP_VERSION
}

res = requests.get(
    _CHART_API_URL,
    headers=headers,
)

data = res.json()

if res.status_code != 200:
            message = f"Request is invalid. response status code={res.status_code}"
            raise FloChartRequestException(message)
entries = {}
music_list = data['data']['trackList'][0]
music_list
entries = {}
music_list = data['data']['trackList']
for item in music_list:
    title = item['name']
    artist = item['representationArtist']['name']
    image = item['album']['imgList'][0]['url'] if item['album']['imgList'] else None
    isNew = item['rank']['newYn'] == "Y" if 'rank' in item and 'newYn' in item['rank'] else False

    # 항목 번호를 문자열로 변환하여 딕셔너리에 저장
    entries[str(item['id'])] = {
        'title': title,
        'artist': artist,
        'image': image,
        'isNew': isNew
    }
print(entries)