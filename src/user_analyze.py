import psycopg2
import pandas as pd

# 데이터베이스 연결 정보
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
cursor.execute("""
            SELECT user_id, array_agg(spotify_tracks_id) AS grouped_spotify_tracks
            FROM search_log_tracks
            GROUP BY user_id;
""")

# 결과 가져오기
slt_data = cursor.fetchall()
user_track_data = pd.DataFrame(slt_data, columns=['user', 'tracks'])

# tracks 컬럼의 값을 전체 리스트로 받고 중복된 값을 제거
all_tracks = list(set(user_track_data['tracks'].explode().tolist()))

# audio_features 테이블에서 id가 all_tracks 리스트에 포함되어 있는 로우 선택
cursor.execute("""
            SELECT id, romantic, adventurous, depressed, powerful, popularity
            FROM audio_features
            WHERE id = ANY(%s);
""", (all_tracks,))

# 결과 가져오기
result = cursor.fetchall()
audio_features_data = pd.DataFrame(result, columns=['id','romantic', 'adventurous', 'depressed', 'powerful', 'popularity'])  
# audio_features_data = pd.DataFrame(result)  

# 결과 출력
print(audio_features_data.head())
print(user_track_data.head())
