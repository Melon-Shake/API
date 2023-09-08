import requests
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
import sys, os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_genie import ChartGenieORM
from model.chart_flo import ChartFloORM
from model.chart_vibe import  VibeORM
from model.chart_bugs import  BugsORM

from model.database import session_scope


class TotalChart(BaseModel) :
    track_name : str
    artist_name : str
    album_name : str
    points : Union[int, float]

with session_scope() as session:
    genieOrms = session.query(ChartGenieORM).all()
    VibeOrms = session.query(VibeORM).all()
    floOrms = session.query(ChartFloORM).all()
    bugsOrms = session.query(BugsORM).all()
    
    integrated_chart = []
    entrie_genie =[]
    for genieOrm in range(len(genieOrms)):
        print(genieOrms)
        test= 11
        debug = 22
        genie_item = ChartGenieORM(**genieOrms)
        print(genie_item)
        genieChart = TotalChart(
            track_name=genieOrm.song_name,
            artist_name=genieOrm.artist_name,
            album_name=genieOrm.album_name,
            points=genieOrm.points
                    )
        entrie_genie.append(genieChart)
        integrated_chart.append(entrie_genie)
    print(integrated_chart)
        
      
    # entrie_vibe =[]
    # for VibeOrm in VibeOrms :
    #     vibeChart = TotalChart(
    #         track_name=VibeOrm.track_title,
    #         artist_name=VibeOrm.artist_name,
    #         album_name=VibeOrm.album_title,
    #         points=VibeOrm.points
    #                 )
    #     entrie_vibe.append(vibeChart)
    #     integrated_chart.append(entrie_vibe)

    # entrie_flo =[]
    # for floOrm in floOrms :
    #     floChart = TotalChart(
    #         track_name=floOrm.track_name,
    #         artist_name=floOrm.artist_name,
    #         album_name=floOrm.album_name,
    #         points=floOrm.points
    #                 )
    #     entrie_flo.append(floChart)
    #     integrated_chart.append(entrie_flo)
        
        
    # entrie_bugs =[]
    # for bugsOrm in bugsOrms :
    #     bugsChart = TotalChart(
    #         track_name=bugsOrm.track_title,
    #         artist_name=bugsOrm.artist_name,
    #         album_name=bugsOrm.album_title,
    #         points=bugsOrm.points
    #                 )
    #     entrie_bugs.append(bugsChart)
    #     integrated_chart.append(entrie_bugs)
        
    # print(integrated_chart)
    # print(integrated_chart[1])
    # integrated = []
    # integrated_chart= integrated.append(entrie_genie, entrie_vibe, entrie_flo, entrie_bugs)
    # print(integrated_chart)
    
    
    
    
    # print(entries)
    
    
    
    
    
    # genieOrm_list = []
    # for item in genieOrm:
    #     name_orm= item.song_name
    #     artist_orm= item.artist_name
    #     album_orm= item.album_name
    #     point_orm= item.points
    # print(print(x))

# else : print(response.status_code)