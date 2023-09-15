import requests
import string
from pydantic import BaseModel
from typing import Dict, List, Union
import sys, os
import pandas as pd
from model.database import engine
from model.chart_genie import ChartGenieORM
from model.chart_flo import ChartFloORM
from model.chart_vibe import VibeORM
from model.chart_bugs import BugsORM
from model.chart_melon import MelonORM
from model.database import session_scope

class TotalChart(BaseModel):
    track_name: str
    artist_name: List[str]
    album_name: str
    points: Union[int, float]
    img_url: str

def generate_total_chart():
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    sys.path.append(root_path)

    with session_scope() as session:
        genieOrms = session.query(ChartGenieORM).all()
        VibeOrms = session.query(VibeORM).all()
        floOrms = session.query(ChartFloORM).all()
        bugsOrms = session.query(BugsORM).all()
        melonOrms = session.query(MelonORM).all()

        # 벅스 top100 차트
        entrie_bugs = [TotalChart(
            track_name=bugsOrm.track_title,
            artist_name=bugsOrm.artist_nms,
            album_name=bugsOrm.album_title,
            points=bugsOrm.points,
            img_url=bugsOrm.album_image_path
        ) for bugsOrm in bugsOrms]

        # 지니 top100 차트
        entrie_genie = [TotalChart(
            track_name=genieOrm.song_name,
            artist_name=genieOrm.artist_name,
            album_name=genieOrm.album_name,
            points=genieOrm.points,
            img_url=genieOrm.album_img_path
        ) for genieOrm in genieOrms]

        # 바이브 top100 차트
        entrie_vibe = [TotalChart(
            track_name=VibeOrm.track_title,
            artist_name=VibeOrm.artist_names,
            album_name=VibeOrm.album_title,
            points=VibeOrm.points,
            img_url=VibeOrm.image_url
        ) for VibeOrm in VibeOrms]

        # flo top100 차트
        entrie_flo = [TotalChart(
            track_name=floOrm.track_name,
            artist_name=floOrm.artist_names,
            album_name=floOrm.album_name,
            points=floOrm.points,
            img_url=floOrm.img_url
        ) for floOrm in floOrms]

        # 멜론 top100 차트
        entrie_melon = [TotalChart(
            track_name=melonOrm.song_name,
            artist_name=melonOrm.artist_names,
            album_name=melonOrm.album_name,
            points=melonOrm.points,
            img_url=melonOrm.album_img
        ) for melonOrm in melonOrms]

        # 5개 차트 종합
        integrated = []
        integrated.extend(entrie_bugs)
        integrated.extend(entrie_flo)
        integrated.extend(entrie_genie)
        integrated.extend(entrie_vibe)
        integrated.extend(entrie_melon)

        # 종합차트 합산 및 정렬
        merged_df = pd.DataFrame([vars(chart) for chart in integrated])
        merged_df['artist_name'] = merged_df['artist_name'].apply(lambda x: ', '.join(x))
        result_df = merged_df.groupby(['track_name', 'artist_name', 'album_name', 'img_url'])['points'].sum().reset_index()
        result_df = result_df.sort_values(by='points', ascending=False).reset_index()

        df = result_df.drop('index', axis=1)

        df.to_sql('total_chart', engine, if_exists='replace', index=True)

# 함수를 호출하여 작업 수행
generate_total_chart()
