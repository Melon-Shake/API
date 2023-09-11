import requests
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
import sys, os
import pandas as pd
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_genie import ChartGenieORM
from model.chart_flo import ChartFloORM
from model.chart_vibe import  VibeORM
from model.chart_bugs import  BugsORM
from model.chart_melon import MelonORM

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
    melonOrms = session.query(MelonORM).all()
    
    # 지니 top100 차트
    entrie_genie = [ TotalChart(
                    track_name=genieOrm.song_name
                    ,artist_name=genieOrm.artist_name
                    ,album_name=genieOrm.album_name
                    ,points=genieOrm.points
                ) for genieOrm in genieOrms]

    # 바이브 top100 차트
    entrie_vibe = [ TotalChart(
                    track_name=VibeOrm.track_title
                    ,artist_name=VibeOrm.artist_name
                    ,album_name=VibeOrm.album_title
                    ,points=VibeOrm.points
                ) for VibeOrm in VibeOrms]

    # flo top100 차트
    entrie_flo = [ TotalChart(
                    track_name=floOrm.track_name,
                    artist_name=floOrm.artist_name,
                    album_name=floOrm.album_name,
                    points=floOrm.points
                    ) for floOrm in floOrms 
                  ]
        
    # 벅스 top100 차트
    entrie_bugs = [ TotalChart(
                        track_name=bugsOrm.track_title
                        ,artist_name=bugsOrm.artist_name
                        ,album_name=bugsOrm.album_title
                        ,points=bugsOrm.points
                    ) for bugsOrm in bugsOrms]
    
    # 멜론 top100 차트
    entrie_melon = [ TotalChart(
                    track_name=melonOrm.song_name
                    ,artist_name=melonOrm.artist_name
                    ,album_name=melonOrm.album_name
                    ,points=melonOrm.points
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
    merged_df = merged_df.apply(lambda x: x.str.replace(r'\s+', '', regex=True) if x.dtype == "object" else x)  #dataframe의 공백제거
    merged_df['track_name'] = merged_df['track_name'].str.replace("’", "'")     # 특수문자 ’ 변경
    # merged_df['track_name'] = merged_df['track_name'].str.replace("'", "")
    merged_df['track_name'] = merged_df['track_name'].str.lower()       #노래제목 영어일때 전체 소문자로변경
    merged_df['artist_name'] = merged_df['artist_name'].str.lower()     #가수이름 영어일때 전체 소문자로 변경   
    result_df = merged_df.groupby(['track_name', 'artist_name', 'album_name'])['points'].sum().reset_index()    # 노래제목,가수이름,앨범이름이 같은경우 점수합산
    # result_df = merged_df.groupby(['track_name', 'artist_name'])['points'].sum().reset_index()
    result_df = result_df.sort_values(by='points', ascending=False).reset_index()       #점수 높은순으로 정렬
    
    df = result_df.drop('index', axis=1)
    print(df)
    
    
    # json_string = df.to_json(orient='records', lines=True, default_handler=str, force_ascii=False)
    # print(json_string)
    # result_df.to_csv('data1.csv', index=False)
    
    
    
    # print(result_df[result_df['artist_name']=='성시경'])
    # search_terms = ['아이유','아이유(IU)','IU','iu']
    # print(result_df[result_df['artist_name'].str.contains('|'.join(search_terms), case=False, regex=True)])
    # merged_df= pd.DataFrame(integrated, columns=['노래','가수','앨범','점수'])
    # merged_df['점수'] = merged_df['점수'].str.extract('(\d+\.\d+)').astype(float)
    # result_df = merged_df.groupby(['가수', '노래', '앨범'])['점수'].sum().reset_index()
    # integrated_chart= integrated.append(entrie_genie, entrie_vibe, entrie_flo, entrie_bugs)
        
    # df_bugs = pd.DataFrame(entrie_bugs, columns=['노래','가수','앨범','점수'])
    # df_vibe = pd.DataFrame(entrie_vibe, columns=['노래','가수','앨범','점수'])
    # df_flo = pd.DataFrame(entrie_flo, columns=['노래','가수','앨범','점수'])
    # df_genie = pd.DataFrame(entrie_genie, columns=['노래','가수','앨범','점수'])
    # df_melon = pd.DataFrame(entrie_bugs, columns=['노래','가수','앨범','점수'])

    # dataframes = [df_bugs, df_genie, df_flo, df_vibe]  # 다른 데이터프레임들도 리스트에 추가

    # # 모든 데이터프레임을 하나로 합치기
    # merged_df = pd.concat(dataframes, ignore_index=True)

    # # '가수', '노래', '앨범' 컬럼을 기준으로 그룹화하여 점수를 합산
    # result_df = merged_df.groupby(['가수', '노래', '앨범'])['점수'].sum().reset_index()
    
    # print(result_df)

