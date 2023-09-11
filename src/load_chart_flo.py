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
        response = response.json()
        responsed_data = response.get('data').get('trackList')
        entries = {}
        for itme in responsed_data:
            for index, item in enumerate(responsed_data):
                track_title = item['name']
                album_title = item['album']['title']
                artists = item.get('artistList')
                artist_pre = []
                for artist in artists:
                    artist_nm = artist['name']
                    artist_pre.append(artist_nm)
                entries[index+1] = [track_title, artist_pre, album_title]
        # for i, e in enumerate(parsed_data) :
        #     entity = ChartFlo(**e)
        #     orm = ChartFloORM(i,entity)
            
        #     with session_scope() as session :
        #         session.add(orm)