## 분석 보고서
# 남/여 별 좋아하는 음원 
# 나이대 별 좋아하는 음원
# 음원 별 좋아하는 성별/나이대
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import psycopg2
import pandas as pd
from tqdm import tqdm
from decimal import Decimal
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from config.db_info import db_params

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
    return plt
    st.pyplot(plt)
    # plt.show()
    
def data_analyze():
    def convert_decimal_to_two_decimal_place(value):
        if isinstance(value, Decimal):
            return round(value, 2)
        return value

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
    

def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "main_page"
    if st.session_state.current_page == "main_page":
        main_page()
    elif st.session_state.current_page =='by_gender':
        by_gender()
    elif st.session_state.current_page =='by_age':
        by_age()    
    elif st.session_state.current_page =='by_track':
        by_track()   
        
def main_page():
    st.title("Melon-Shake Data Analyze")
    if st.button('연령대 별 특성 레이더 차트'):
        st.session_state.current_page='by_age'
        st.experimental_rerun()
    if st.button("성별에 따른 특성 선호도 분석"):
        st.session_state.current_page='by_gender'
        st.experimental_rerun()

    if st.button('음원에 대한 연령대별, 성별 선호도'):
        st.session_state.current_page='by_track'
        st.experimental_rerun()
def by_gender():
    num_features = len(grouped_by_gender.columns)
    # 각 변수의 각도 계산
    angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False).tolist()
    angles += angles[:1]

    # 그래프 설정
    plt.figure(figsize=(18, 6))

    # F vs M 비교 그래프
    plt.subplot(1, 3, 1, polar=True)
    for gender in ['F', 'M']:
        values = grouped_by_gender.loc[gender].values.tolist()
        values += values[:1]
        plt.fill(angles, values, alpha=0.5, label=gender)
    plt.xticks(angles[:-1], grouped_by_gender.columns)
    plt.title('F vs M Radar Chart')
    plt.ylim(0, 1)
    plt.legend()

    # F에 대한 레이더 차트
    plt.subplot(1, 3, 2, polar=True)
    values_F = grouped_by_gender.loc['F'].values.tolist()
    values_F += values_F[:1]
    plt.fill(angles, values_F, 'b', alpha=0.5)
    plt.xticks(angles[:-1], grouped_by_gender.columns)
    plt.title('F Radar Chart')
    plt.ylim(0, 1)

    # M에 대한 레이더 차트
    plt.subplot(1, 3, 3, polar=True)
    values_M = grouped_by_gender.loc['M'].values.tolist()
    values_M += values_M[:1]
    plt.fill(angles, values_M, 'r', alpha=0.5)
    plt.xticks(angles[:-1], grouped_by_gender.columns)
    plt.title('M Radar Chart')
    plt.ylim(0, 1)

    # 그래프 표시
    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)
    
    if st.button("BACK"):
        st.session_state.current_page = "main_page"
        st.experimental_rerun()
def by_age():
    # 연령대 선택
    selected_age = st.radio('연령대 선택', grouped_age.index)

    # 선택한 연령대에 따라 레이더 차트 그리기
    if selected_age in grouped_age.index:
        values = grouped_age.loc[selected_age].values.tolist()
        features = grouped_age.columns.tolist()

        # 레이더 차트 그리기
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
        ax.fill(features, values, alpha=0.5)
        ax.set_title(f'Radar Chart of {selected_age}-year-old Age Group Characteristics')
        st.pyplot(fig)
    else:
        st.write('선택한 연령대에 대한 데이터가 없습니다.')
    if st.button("BACK"):
        st.session_state.current_page = "main_page"
        st.experimental_rerun()
def by_track():  
    id = st.text_input('음원 ID를 입력 해 주세요')
    if id:
        st.pyplot(show_plt_by_track_id(id))
    if st.button("BACK"):
        st.session_state.current_page = "main_page"
        st.experimental_rerun()
if __name__ == "__main__":
    main()