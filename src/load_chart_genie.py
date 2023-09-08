import requests

import sys
import os
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
                                'pg_size': '200'
                             }
                            )

    if response.status_code == 200 :
        responsed_data = response.json().get('DataSet').get('DATA')

        for e in responsed_data :
            entity = ChartGenie(**e)
            orm = ChartGenieORM(entity)

            if entity.SONG_ID == '102664199' :
                print(entity.SONG_NAME)

            if entity.ARTIST_ID == '80197389' :
                print(entity.ARTIST_NAME)

            if entity.ALBUM_ID == '84193518' :
                print(entity.ALBUM_NAME)
                print(entity.ALBUM_IMG_PATH)

            # with session_scope() as session :
            #     session.add(orm)

    else : print(response.status_code)