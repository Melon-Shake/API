from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys, numpy as np, pandas as pd, json, requests, re
from datetime import datetime

app = FastAPI()

_APP_VERSION = "6.5.8.1"
_CP_ID = "AS40"
_USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
_CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"

@app.post("/chart/melon_chart/")
def get_melonChat():

    class MelonChartRequestException(Exception):
        pass

    class MelonChartParseException(Exception):
        pass

    class ChartEntry:
        def __init__(self, title: str, artist: str, image: str, lastPos: int, rank: int, isNew: bool):
            self.title = title
            self.artist = artist
            self.image = image
            self.lastPos = lastPos
            self.rank = rank
            self.isNew = isNew

        def __repr__(self):
            return f"{self.__class__.__module__}.{self.__class__.__name__}(title={self.title!r}, artist={self.artist!r})"
    
        def __str__(self):
            if self.title:
                s = f"'{self.title}' by {self.artist}"
            else:
                s = f"{self.artist}"

            if sys.version_info.major < 3:
                return s.encode(getattr(sys.stdout, "encoding", "") or "utf8")
            else:
                return s

        def json(self):
            """json 형태로 반환"""
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)  
    
    def _getResizedImage(url, imageSize):
        pattern = r"resize/\d+"
        return re.sub(pattern, f"resize/{imageSize}", url)


    headers = {"User-Agent": _USER_AGENT}
    res = requests.get(_CHART_API_URL, headers=headers)
    data = res.json()
    name = data["response"]["PAGE"]
    date = f"{data['response']['RANKDAY']} {data['response']['RANKHOUR']}"
    date_format = "%Y.%m.%d %H:%M"
    pre_date = datetime.strptime(date, date_format)
    entries = []

    for item in data['response']['SONGLIST']:
        entry = ChartEntry(
            title=item['SONGNAME'],
            artist=item['ARTISTLIST'][0]['ARTISTNAME'],
            image=_getResizedImage(item['ALBUMIMG'], 256),
            rank=int(item["CURRANK"]),
            lastPos=int(item["PASTRANK"]),
            isNew=item["RANKTYPE"] == "NEW"
        )
        entries.append(entry)
    
    if res.status_code == 200:
        entries_json = json.dumps(entries, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        return entries_json
    else:
        return {"error": "Spotify API request failed"}
    
    
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