import requests

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_flo import ChartFlo, ChartFloORM
from model.database import session_scope

if __name__ == '__main__':

    response = requests.get("https://api.music-flo.com/display/v1/browser/chart/1/list?mixYn=N"
                      ,headers = {"User-Agent": "okhttp/4.9.2",
                                  "x-gm-app-name":"FLO",
                                   "x-gm-app-version": ""
                                }
                      )

    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = responsed_data.get('data').get('trackList')

        for e in parsed_data :
            entity = ChartFlo(**e)
            orm = ChartFloORM(entity)
            x = orm.album.imgList[0].url
            print(type(x))
            print(x)