import requests
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
import sys, os
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
                                'pgsize': '100'
                             }
                            )

    if response.status_code == 200 :
        responsed_data = response.json().get('DataSet').get('DATA')
        for e in responsed_data :
            entity = ChartGenie(**e)
            orm = ChartGenieORM(entity)

            # with session_scope() as session :
            #     session.add(orm)
        
        class TotalChart(BaseModel) :
            track_name : str
            artist_name : str
            album_name : str
            points : Union[int, float]
        
        with session_scope() as session:
            genieOrms = session.query(ChartGenieORM).all()
            entries =[]
            for genieOrm in genieOrms :
                genieChart = TotalChart(
                    track_name=genieOrm.song_name,
                    artist_name=genieOrm.artist_name,
                    album_name=genieOrm.album_name,
                    points=genieOrm.points
                           )
                entries.append(genieChart)
            print(entries)
            
            
            
            
            
            # genieOrm_list = []
            # for item in genieOrm:
            #     name_orm= item.song_name
            #     artist_orm= item.artist_name
            #     album_orm= item.album_name
            #     point_orm= item.points
            # print(print(x))

    # else : print(response.status_code)