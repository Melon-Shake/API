from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import psycopg2
from model.jun_model import playlist



def make_playlist(data:playlist,song_count,db_params):
    email = data.email
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    value = (email,)
    cursor.execute(user_query, value)
    user_query_result = cursor.fetchone()
    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None
    
    user_query ="""
                   select user_id, f1,f2,f3,f4,f5 from user_features where user_id = %s;
    """
    user_values = (user_id,)
    # 컬럼 정보 조회 쿼리 실행
    cursor.execute(user_query, user_values)

    # 결과 가져오기
    user_data = pd.DataFrame(cursor.fetchall(),columns=['user_id','romantic', 'adventurous', 'depressed','powerful', 'popularity'])

    # 컬럼 정보 조회 쿼리 실행
    cursor.execute("""
                select id, romantic, adventurous, depressed,powerful, popularity from audio_features;
    """)

    # 결과 가져오기
    track_data = pd.DataFrame(cursor.fetchall(),columns=['track_id','romantic', 'adventurous', 'depressed','powerful', 'popularity'])

    user_features = user_data[['romantic', 'adventurous', 'depressed', 'powerful', 'popularity']]
    track_features = track_data[['romantic', 'adventurous', 'depressed', 'powerful', 'popularity']]
    similarities = cosine_similarity(user_features, track_features)

    N = song_count  # 추천할 곡의 수
    top_n_indices = similarities.argsort()[0][-N:][::-1]

    recommended_playlist = []

    for i, song_index in enumerate(top_n_indices):
        recommended_song_id = track_data.loc[song_index, 'track_id']
        similarity_score = similarities[0][song_index]
        recommended_playlist.append(recommended_song_id)
    



    conn.commit()
    cursor.close()
    conn.close()
    return recommended_playlist
