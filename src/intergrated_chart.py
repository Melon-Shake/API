import requests
import string
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
import sys, os
import pandas as pd
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import engine


from model.chart_genie import ChartGenieORM
from model.chart_flo import ChartFloORM
from model.chart_vibe import  VibeORM
from model.chart_bugs import  BugsORM
from model.chart_melon import MelonORM

from model.database import session_scope


class TotalChart(BaseModel) :
    track_name : str
    artist_names : List[str]
    album_name : str
    points : Union[int, float]
    img_url : str

with session_scope() as session:
    genieOrms = session.query(ChartGenieORM).all()
    VibeOrms = session.query(VibeORM).all()
    floOrms = session.query(ChartFloORM).all()
    bugsOrms = session.query(BugsORM).all()
    melonOrms = session.query(MelonORM).all()
    
    # 벅스 top100 차트
    entrie_bugs = [ TotalChart(
                        track_name=bugsOrm.track_name
                        ,artist_names=bugsOrm.artist_names
                        ,album_name=bugsOrm.album_name
                        ,points=bugsOrm.points
                        ,img_url=bugsOrm.img_url
                    ) for bugsOrm in bugsOrms]
    # 지니 top100 차트
    entrie_genie = [ TotalChart(
                    track_name=genieOrm.track_name
                    ,artist_names=genieOrm.artist_names
                    ,album_name=genieOrm.album_name
                    ,points=genieOrm.points
                    ,img_url=genieOrm.img_url
                ) for genieOrm in genieOrms]

    # 바이브 top100 차트
    entrie_vibe = [ TotalChart(
                    track_name=VibeOrm.track_name
                    ,artist_names=VibeOrm.artist_names
                    ,album_name=VibeOrm.album_name
                    ,points=VibeOrm.points
                    ,img_url=VibeOrm.img_url
                ) for VibeOrm in VibeOrms]

    # flo top100 차트
    entrie_flo = [ TotalChart(
                    track_name=floOrm.track_name,
                    artist_names=floOrm.artist_names,
                    album_name=floOrm.album_name,
                    points=floOrm.points,
                    img_url=floOrm.img_url
                    ) for floOrm in floOrms 
                  ]
        
    
    # 멜론 top100 차트
    entrie_melon = [ TotalChart(
                    track_name=melonOrm.track_name
                    ,artist_names=melonOrm.artist_names
                    ,album_name=melonOrm.album_name
                    ,points=melonOrm.points
                    ,img_url=melonOrm.img_url
                ) for melonOrm in melonOrms]
        
    # 5개 차트 종합
    integrated = []
    integrated.extend(entrie_bugs)
    integrated.extend(entrie_flo)
    integrated.extend(entrie_genie)
    integrated.extend(entrie_vibe)
    integrated.extend(entrie_melon)
    
    # 종합차트 합산 및 정렬
    merged_df = pd.DataFrame([vars(chart) for chart in integrated])     #dataframe 형식으로 변환
    merged_df['artist_names'] = merged_df['artist_names'].apply(lambda x: ', '.join(x))
    result_df = merged_df.groupby(['track_name', 'album_name', 'img_url']).agg({'artist_names': 'first', 'points': 'sum'}).reset_index()
    result_df = merged_df.groupby(['track_name', 'artist_names', 'album_name','img_url'])['points'].sum().reset_index()    # 노래제목,가수이름,앨범이름,앨범이미지 같은경우 점수합산
    result_df = result_df.sort_values(by='points', ascending=False).reset_index()       #점수 높은순으로 정렬
    
    df = result_df.drop('index', axis=1)    #index 컬럼 제거

    df.to_sql('total_chart', engine, if_exists='replace', index=True)   #데이터프레임을 데이터베이스 'total_chart'로 생성

    
    
    
    # # '가수', '노래', '앨범' 컬럼을 기준으로 그룹화하여 점수를 합산
    # result_df = merged_df.groupby(['가수', '노래', '앨범'])['점수'].sum().reset_index()


