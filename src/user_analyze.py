import psycopg2
import pandas as pd
from tqdm import tqdm
from config.db_info import db_params

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
audio_features_data = pd.DataFrame(result, columns=['id', 'romantic', 'adventurous', 'depressed', 'powerful', 'popularity'])

for users in tqdm(range(user_track_data.shape[0])):
    romantic = 0.0
    adventurous = 0.0
    depressed = 0.0
    powerful = 0.0
    popularity = 0.0
    user_id = int(user_track_data.loc[users]['user'])

    for i, track in enumerate(user_track_data.loc[users][1]):
        rows = audio_features_data[audio_features_data['id'] == track]
        romantic += float(rows['romantic'].values[0])
        adventurous += float(rows['adventurous'].values[0])
        depressed += float(rows['depressed'].values[0])
        powerful += float(rows['powerful'].values[0])
        popularity += float(rows['popularity'].values[0])

    val = [user_id, romantic / len(user_track_data.loc[users][1]), adventurous / len(user_track_data.loc[users][1]), depressed / len(user_track_data.loc[users][1]), powerful / len(user_track_data.loc[users][1]), popularity / len(user_track_data.loc[users][1])]
    query = """
        INSERT INTO user_features (user_id, f1, f2, f3, f4, f5)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
        user_id = EXCLUDED.user_id,
        f1 = EXCLUDED.f1,
        f2 = EXCLUDED.f2,
        f3 = EXCLUDED.f3,
        f4 = EXCLUDED.f4,
        f5 = EXCLUDED.f5;
    """
    cursor.execute(query, val)

conn.commit()

cursor.close()
conn.close()
