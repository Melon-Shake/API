## audio_features update
import psycopg2
import pandas as pd
from tqdm import tqdm
import decimal



## 호출하면 spotify_audio_features 테이블에서 
def audio_features_update():
    def decimal_to_float(dataframe):
        for column in dataframe.columns:
            if dataframe[column].dtype == decimal.Decimal:
                try:
                    dataframe[column] = dataframe[column].apply(lambda x: float(x))
                except ValueError:
                    pass  # 문자열을 float로 변환할 수 없는 경우 건너뜁니다.
        return dataframe
    
    def normalize_rows(df):
        normalized_df = df.copy()
        for index, row in df.iterrows():
            min_val = row.min()
            max_val = row.max()
            normalized_df.loc[index] = (row - min_val) / (max_val - min_val)
        
        return normalized_df
    def audio_features_popularity_update():
        def sum_chart_points(id):
            data_frames = [chart_melon, chart_bugs, chart_flo, chart_genie, chart_vibe]  
            total_score = 0
            for df in data_frames:
                if id in df['id'].values:
                    total_score += df.loc[df['id'] == id, 'points'].sum()
            return id, total_score
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
        cursor.execute("SELECT track_id, points FROM chart_bugs")
        chart_bugs = decimal_to_float(pd.DataFrame(cursor.fetchall(),columns=['id','points']))
        cursor.execute("SELECT track_id, points FROM chart_flo")
        chart_flo = decimal_to_float(pd.DataFrame(cursor.fetchall(),columns=['id','points']))
        cursor.execute("SELECT track_id, points FROM chart_genie")
        chart_genie = decimal_to_float(pd.DataFrame(cursor.fetchall(),columns=['id','points']))
        cursor.execute("SELECT track_id, points FROM chart_melon")
        chart_melon = decimal_to_float(pd.DataFrame(cursor.fetchall(),columns=['id','points']))
        cursor.execute("SELECT track_id, points FROM chart_vibe")
        chart_vibe = decimal_to_float(pd.DataFrame(cursor.fetchall(),columns=['id','points']))

        cursor.execute("select id from audio_features")
        ad_fe_data = cursor.fetchall()
        ## ad_fe_data[0][0] = 3wahCFMh2d1ksY49GcnVbQ
        
        for pop in range(len(ad_fe_data)):
            id = ad_fe_data[pop][0]
            point = sum_chart_points(id)[1]
            cursor.execute(f"""
                            UPDATE audio_features
                            SET popularity = {point}
                            WHERE id = '{id}';
                           """)
        
        cursor.execute("""
                        SELECT id, popularity
                        FROM audio_features
                        WHERE popularity <> 0;

                    """)
        pop_data = pd.DataFrame(cursor.fetchall(),columns=["id",'popularity'])
        pop_data = decimal_to_float(pop_data)
        # 정규화
        min_value = pop_data['popularity'].min()
        max_value = pop_data['popularity'].max()


        pop_data['popularity'] = 0.1 + (pop_data['popularity'] - min_value) / (max_value - min_value) * 0.9
        for i in range(pop_data.shape[0]):
            id = pop_data.loc[i][0]
            point = pop_data.loc[i][1]
            cursor.execute(f"""
                            UPDATE audio_features
                            SET popularity = {point}
                            WHERE id = '{id}';
                        """)

        conn.commit()
        cursor.close()
        conn.close()

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
                select id, acousticness, danceability, energy, instrumentalness, liveness,loudness, speechiness, tempo, valence 
                FROM spotify_audio_features
                WHERE is_analyze = false OR is_analyze IS NULL;
    """)

    # 결과 가져오기
    column_info = cursor.fetchall()
    # 컬럼 정보 조회 쿼리 실행
    cursor.execute("""
                select id, romantic_words, adventurous_words, powerful_words, depressed_words from lyrics
    """)

    # 결과 가져오기
    ly_column_info = cursor.fetchall()
    normalized_data = []
    for row in column_info:
        normalized_row = [row[0]] + [float(value) if value is not None else None for value in row[1:]]
        normalized_data.append(normalized_row)

    # print(column_info)
    # 기본 전처리
    column_info2 = column_info 
    columns = ['id','acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    df = pd.DataFrame(column_info2, columns=columns)
    df['tempo']= df['tempo']/180
    # print(df.head())
    ly_df = pd.DataFrame(ly_column_info,columns=['spotify_tracks_id','romantic','adventurous','powerful','depressed'])
    # print(ly_df)
    df2 = normalize_rows(df.iloc[:, 1:])

    ly_df2 = normalize_rows(ly_df.iloc[:, 1:])
    ly_df2['id']= ly_df['spotify_tracks_id']
    ly_df2 = decimal_to_float(ly_df2)
    df2['id'] = df['id']
    df2=df2.drop_duplicates(subset='id', keep='first')
    # 값연산
    df3 = pd.DataFrame()
    df3['romantic'] = (df2['acousticness'] + df2['valence']) / 2
    df3['adventurous'] =( df2['danceability'] + df2['tempo'])/2
    df3['depressed'] = (1 - df2['energy']) * (1 - df2['loudness'])
    df3['powerful'] =  (df2['energy'] + (1 - df2['instrumentalness'])) / 2
    df3['id'] = df['id']
    df3 = decimal_to_float(df3)

    # id 기준으로 df 합산
    merged_df = pd.concat([df3, ly_df2], ignore_index=True)
    result = merged_df.groupby('id')[['romantic', 'adventurous', 'depressed','powerful']].sum().reset_index()

    for i in tqdm(range(result.shape[0])):
        #데이터 삽입
        insert_query = """
            INSERT INTO audio_features (romantic, adventurous, depressed, powerful, id) values (%s, %s, %s, %s, %s);
        """
        
        id = df3.iloc[i]['id']
        insert_values = []
        for val in df3.iloc[i].values:
            if isinstance(val, str):
                # print(val)
                insert_values.append(val)
            else:
                insert_values.append(float(val))
        cursor.executemany(insert_query, [insert_values])
        conn.commit()
        # if df3.iloc[i]['id'] == '4Dr2hJ3EnVh2Aaot6fRwDO':
        #     return
        #is_analyze 업데이트
        flag_update_query = f"""
        UPDATE spotify_audio_features
        SET is_analyze = True
        WHERE id = '{id}';
        """
        cursor.execute(flag_update_query)
        conn.commit()


    cursor.close()
    conn.close()
    audio_features_popularity_update()
    

# user_features_update
import psycopg2
import pandas as pd
from tqdm import tqdm

def user_features_update():
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
    audio_features_data = pd.DataFrame(result, columns=['id', 'romantic', 'adventurous', 'depressed', 'powerful', 'popularity'])

    for users in tqdm(range(user_track_data.shape[0])):
        romantic = 0.0
        adventurous = 0.0
        depressed = 0.0
        powerful = 0.0
        popularity = 0.0
        user_id = int(user_track_data.loc[users]['user'])
        print(user_track_data.loc[users])
        for i, track in enumerate(user_track_data.loc[users][1]):
            print(i,track)
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


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def make_playlist(user_id, song_count):
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
                select user_id, f1,f2,f3,f4,f5 from user_features where user_id = {user_id};
    """)

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
        recommended_song_id = track_data.loc[song_index, 'SongID']
        similarity_score = similarities[0][song_index]
        recommended_playlist.append(recommended_song_id)

    
    conn.commit()
    cursor.close()
    conn.close()
    return user_data ,track_data