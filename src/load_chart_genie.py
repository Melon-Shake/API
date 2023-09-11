import requests

import sys
import os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_genie import ChartGenie, ChartGenieORM
from model.database import session_scope

if __name__ == '__main__' :
    response = requests.post('https://app.genie.co.kr/chart/j_RealTimeRankSongList.json'
                             ,headers={
                                 'Content_Type' : 'application/x-www-form-urlencoded'
                             }
                             ,data={
                                'pgSize': '100'
                             }
                            )

    if response.status_code == 200 :
        responsed_data = response.json().get('DataSet').get('DATA')

        entries = {}
        for itme in responsed_data:
            for index, item in enumerate(responsed_data):
                # 제목 디코딩
                pre_track_title = item['SONG_NAME']
                track_title = urllib.parse.unquote(pre_track_title)
                
                # 아티스트 디코딩
                pre_artists = item.get('ARTIST_NAME')
                artists = urllib.parse.unquote(pre_artists)  # URL 디코딩

                entries[index+1] = [track_title, artists]
        print(entries)
    #     for e in responsed_data :
    #         entity = ChartGenie(**e)
    #         orm = ChartGenieORM(entity)

    #         with session_scope() as session :
    #             session.add(orm)

    # else : print(response.status_code)