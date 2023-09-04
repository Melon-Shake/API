from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from datetime import datetime
import sys, numpy as np, pandas as pd, json, requests, re

app = FastAPI()

_USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
_IMAGE_PREFIX_URL = "https://image.bugsm.co.kr/album/images"
_CHART_API_URL = "https://m.bugs.co.kr/api/getChartTrack"

headers = {"User-Agent": _USER_AGENT}
res = requests.get(_CHART_API_URL, headers=headers)
data = res.json()

update_time = f"{data['response']['RANKDAY']} {data['response']['RANKHOUR']}"
entries = {}
song_list = data['response']['SONGLIST']

for item in range(len(song_list)):
    song_name = song_list[item]['SONGNAME'] 
    artist = song_list[item]['ARTISTLIST'][0]['ARTISTNAME']
    image = song_list[item]['ALBUMIMG']
    # rank = song_list[item]['CURRANK']
    pastrank = song_list[item]['PASTRANK']
    isNew = song_list[item]['RANKTYPE'] == "NEW"

    entries[str(item+1)]= [song_name, artist, image, pastrank, isNew]
  
print(entries)


# @app.post("/chart/melon_chart/")
# def get_melonChat():
#     headers = {"User-Agent": _USER_AGENT}
#     res = requests.get(_CHART_API_URL, headers=headers)
#     data = res.json()

#     ## 멜론차트_TOP100NOW
#     page_name = data["response"]["PAGE"]
    
#     ## 2023.08.31 15:00
#     update_time = f"{data['response']['RANKDAY']} {data['response']['RANKHOUR']}"
    
#     ## datetime.datetime(2023, 8, 31, 15, 0)
#     date_format = "%Y.%m.%d %H:%M"
#     pre_date = datetime.strptime(update_time, date_format)
    
#     entries = {}
#     song_list = data['response']['SONGLIST'] 

#     for item in range(len(song_list)):
#         song_name = song_list[item]['SONGNAME'] 
#         artist = song_list[item]['ARTISTLIST'][0]['ARTISTNAME']
#         image = song_list[item]['ALBUMIMG']
#         # rank = song_list[item]['CURRANK']
#         pastrank = song_list[item]['PASTRANK']
#         isNew = song_list[item]['RANKTYPE'] == "NEW"

#         entries[str(item+1)]= [song_name, artist, image, pastrank, isNew]

#     return entries