from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys, numpy as np, pandas as pd, json, requests, re
from datetime import datetime

app = FastAPI()

_APP_VERSION = "6.5.8.1"
_CP_ID = "AS40"
_USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
_CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"

class MelonChartRequestException(Exception):
    pass

class MelonChartParseException(Exception):
    pass

@app.post("/chart/melon_chart/")
def get_melonChat():
    headers = {"User-Agent": _USER_AGENT}
    res = requests.get(_CHART_API_URL, headers=headers)
    data = res.json()

    ## 멜론차트_TOP100NOW
    page_name = data["response"]["PAGE"]
    
    ## 2023.08.31 15:00
    update_time = f"{data['response']['RANKDAY']} {data['response']['RANKHOUR']}"
    
    ## datetime.datetime(2023, 8, 31, 15, 0)
    date_format = "%Y.%m.%d %H:%M"
    pre_date = datetime.strptime(update_time, date_format)
    
    entries = {}
    song_list = data['response']['SONGLIST'] 

    # len(data['response']['SONGLIST'])

    for item in range(len(song_list)):
        song_name = song_list[item]['SONGNAME'] 
        artist = song_list[item]['ARTISTLIST'][0]['ARTISTNAME']
        image = song_list[item]['ALBUMIMG']
        # rank = song_list[item]['CURRANK']
        pastrank = song_list[item]['PASTRANK']
        isNew = song_list[item]['RANKTYPE'] == "NEW"

        entries[str(item+1)]= [song_name, artist, image, pastrank, isNew]
        # entries["top"+ item]= [data['response']['SONGLIST'][item]['SONGNAME']]

    return entries
    
    # try:
    #     entries_json = json.dumps(entries, default=lambda o: o.__dict__, sort_keys=True, indent=4,ensure_ascii=False)
    #     # output_data = json.dumps(chart_data, default=lambda o: o.__dict__,sort_keys=True, indent=4, ensure_ascii=False)
    #     return chart_data
    #     # return JSONResponse(content=chart_data.__dict__)
    # except (MelonChartRequestException, MelonChartParseException) as e:
    #     raise HTTPException(status_code = 500, detail=str(e))
    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=9799)