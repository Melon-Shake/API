import requests
import string
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
import sys, os
import pandas as pd
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.database import engine
from model.chart_genie import GenieORM
from model.chart_flo import FloORM
from model.chart_vibe import  VibeORM
from model.chart_bugs import  BugsORM
from model.chart_melon import MelonORM
from model.database import session_scope
import src.search_spotify as Search

class TotalChart(BaseModel) :
    track_name : str
    track_id : str
    artist_names : str
    artist_ids : List[str]
    album_name : str
    album_id : str
    points : Union[int, float]
    img_url : str

with session_scope() as session:
    genieOrms = session.query(GenieORM).all()
    VibeOrms = session.query(VibeORM).all()
    floOrms = session.query(FloORM).all()
    bugsOrms = session.query(BugsORM).all()
    melonOrms = session.query(MelonORM).all()
    
    # 벅스 top100 차트
    entrie_bugs = [ TotalChart(
                        track_name=bugsOrm.track_name
                        ,track_id=bugsOrm.track_id
                        ,artist_names=bugsOrm.artist_names
                        ,artist_ids=bugsOrm.artist_ids
                        ,album_name=bugsOrm.album_name
                        ,album_id=bugsOrm.album_id
                        ,points=bugsOrm.points
                        ,img_url=bugsOrm.img_url
                    ) for bugsOrm in bugsOrms]
    # 지니 top100 차트
    entrie_genie = [ TotalChart(
                    track_name=genieOrm.track_name
                    ,track_id=genieOrm.track_id
                    ,artist_names=genieOrm.artist_names
                    ,artist_ids=genieOrm.artist_ids
                    ,album_name=genieOrm.album_name
                    ,album_id=genieOrm.album_id
                    ,points=genieOrm.points
                    ,img_url=genieOrm.img_url
                ) for genieOrm in genieOrms]

    # 바이브 top100 차트
    entrie_vibe = [ TotalChart(
                    track_name=VibeOrm.track_name
                    ,track_id=VibeOrm.track_id
                    ,artist_names=VibeOrm.artist_names
                    ,artist_ids=VibeOrm.artist_ids
                    ,album_name=VibeOrm.album_name
                    ,album_id=VibeOrm.album_id
                    ,points=VibeOrm.points
                    ,img_url=VibeOrm.img_url
                ) for VibeOrm in VibeOrms]
    # flo top100 차트
    entrie_flo = [ TotalChart(
                     track_name=floOrm.track_name
                    ,track_id=floOrm.track_id
                    ,artist_names=floOrm.artist_names
                    ,artist_ids=floOrm.artist_ids
                    ,album_name=floOrm.album_name
                    ,album_id=floOrm.album_id
                    ,points=floOrm.points
                    ,img_url=floOrm.img_url
                    ) for floOrm in floOrms]
     # 멜론 top100 차트
    entrie_melon = [ TotalChart(
                    track_name=melonOrm.track_name
                    ,track_id=melonOrm.track_id
                    ,artist_names=melonOrm.artist_names
                    ,artist_ids=melonOrm.artist_ids
                    ,album_name=melonOrm.album_name
                    ,album_id=melonOrm.album_id
                    ,points=melonOrm.points
                    ,img_url=melonOrm.img_url
                ) for melonOrm in melonOrms]
    
    integrated = []
    integrated.extend(entrie_bugs)
    integrated.extend(entrie_flo)
    integrated.extend(entrie_genie)
    integrated.extend(entrie_vibe)
    integrated.extend(entrie_melon)
    
    merged_df = pd.DataFrame([vars(chart) for chart in integrated])     #dataframe 형식으로 변환
    merged_df['artist_ids'] = merged_df['artist_ids'].apply(lambda x: ', '.join(x))
    result_df = merged_df.groupby(['track_name', 'artist_names', 'album_name','img_url','track_id','artist_ids','album_id'])['points'].sum().reset_index()    # 노래제목,가수이름,앨범이름,아이디들이 같은경우 점수합산
    track_ids = result_df['track_id'].tolist()
    

    result_df = result_df.sort_values(by='points', ascending=False).reset_index()       #점수 높은순 정렬
    df = result_df.drop('index', axis=1)
    df.to_sql('total_chart', engine, if_exists='replace', index=True)   #데이터프레임을 데이터베이스 'total_chart'로 생성