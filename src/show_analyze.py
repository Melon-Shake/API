## 분석 보고서
# 남/여 별 좋아하는 음원 
# 나이대 별 좋아하는 음원
# 음원 별 좋아하는 성별/나이대
import psycopg2
import pandas as pd
from tqdm import tqdm
from decimal import Decimal
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def data_analyze():
    def convert_decimal_to_two_decimal_place(value):
        if isinstance(value, Decimal):
            return round(value, 2)
        return value
    
    db_params = {
        'user': 'postgres',
        'password': '12345678',
        'host': 'database-1.coea55uwjt5p.ap-northeast-1.rds.amazonaws.com',
        'port': '5432',
        'database': 'postgres'
    }

    # 데이터베이스에 연결
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # 컬럼 정보 조회 쿼리 실행
    cursor.execute(f"""
                select gender,age,user_id from user_properties;
    """)

    # 결과 가져오기
    user_properties_data = pd.DataFrame(cursor.fetchall(),columns=['gender','age','user_id'])
    
    cursor.execute(f"""
                select spotify_tracks_id, user_id from search_log_tracks;
    """)
    track_logs = pd.DataFrame(cursor.fetchall(),columns=['spotify_tracks_id','user_id'])
  
    cursor.execute(f"""
                select id, romantic, adventurous, depressed, powerful, popularity from audio_features;
    """)
    track_features = pd.DataFrame(cursor.fetchall(),columns=['spotify_tracks_id', 'romantic', 'adventurous', 'depressed', 'powerful', 'popularity'])
    track_features= track_features.applymap(convert_decimal_to_two_decimal_place)
                                  
    result_df = track_logs.merge(user_properties_data, on='user_id', how='left')
    # result_df = result_df.merge(track_features, on='spotify_tracks_id', how='left')
    result_df2 = result_df.merge(track_features, on='spotify_tracks_id', how='left')
    conn.commit()
    cursor.close()
    conn.close()
    return user_properties_data, track_logs,track_features,result_df,result_df2
    
a = data_analyze()
df = a[-1].dropna().reset_index(drop=True)
grouped_by_gender = df.groupby('gender')[['romantic', 'adventurous', 'depressed', 'powerful', 'popularity']].mean()

# 나이를 10대 단위로 나누어 새로운 컬럼 'age_group'을 생성
df['age_group'] = (df['age'] // 10) * 10

# 나이 그룹으로 그룹화하고 각 그룹의 'romantic', 'adventurous', 'depressed', 'powerful', 'popularity'의 평균 계산
grouped_age = df.groupby('age_group')[['romantic', 'adventurous', 'depressed', 'powerful', 'popularity']].mean()

def show_plt_by_track_id(target_track_id):
    # target_track_id = '3ucfniv4fLB3RPA6N9iLM2'

    # 입력한 곡 ID에 대한 데이터 추출
    song_data = df[df['spotify_tracks_id'] == target_track_id]

    # 나이대 별로 그룹화
    song_data['age_group'] = (song_data['age'] // 10) * 10

    # 성별에 따라 그룹화한 후 각 그룹의 개수를 계산
    grouped = song_data.groupby(['age_group', 'gender']).size().unstack()

    # 그래프에 영어 레이블 설정
    plt.figure(figsize=(10, 6))
    grouped.plot(kind='line', marker='o', color=['blue', 'red'])
    plt.title(f'Track ID: {target_track_id} Age Group Male vs Female Ratio')
    plt.xlabel('Age Group (in 10s)')
    plt.ylabel('Number of Users')
    plt.xticks(grouped.index)
    plt.legend(title='Gender', labels=['Male', 'Female'])
    plt.grid(True)
    plt.show()
    
