## db에서 데이터 읽기, row별로 정규화, 연산, 분석 결과에 삽입

# 컬럼이름찾기
import psycopg2
import pandas as pd

## 호출하면 spotify_audio_features 테이블에서 
def audio_features_update():
    def normalize_rows(df):
        normalized_df = df.copy()
        for index, row in df.iterrows():
            min_val = row.min()
            max_val = row.max()
            normalized_df.loc[index] = (row - min_val) / (max_val - min_val)
        
        return normalized_df


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
                select id, acousticness, danceability, energy, instrumentalness, liveness,loudness, speechiness, tempo, valence from spotify_audio_features 
    """)

    # 결과 가져오기
    column_info = cursor.fetchall()
    # 컬럼 정보 조회 쿼리 실행
    cursor.execute("""
                select track_id, romantic_words, adventurous_words, powerful_words, depresed_words from lyrics
    """)

    # 결과 가져오기
    ly_column_info = cursor.fetchall()
    normalized_data = []
    for row in column_info:
        normalized_row = [row[0]] + [float(value) if value is not None else None for value in row[1:]]
        normalized_data.append(normalized_row)


    # 기본 전처리
    column_info2 = column_info 
    columns = ['id','acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    df = pd.DataFrame(column_info2, columns=columns)
    df['tempo']= df['tempo']/180

    ly_df = pd.DataFrame(ly_column_info,columns=['track_id','romantic','adventurous','powerful','depresed'])

    df2 = normalize_rows(df.iloc[:, 1:])

    ly_df2 = normalize_rows(ly_df.iloc[:, 1:])
    ly_df2['id']= ly_df['track_id']
    df2['id'] = df['id']

    # 값연산
    df3 = pd.DataFrame()
    df3['romantic'] = (df2['acousticness'] + df2['valence']) / 2
    df3['adventurous'] =( df2['danceability'] + df2['tempo'])/2
    df3['depresed'] = (1 - df2['energy']) * (1 - df2['loudness'])
    df3['powerful'] =  (df2['energy'] + (1 - df2['instrumentalness'])) / 2
    df3['id'] = df['id']

    # id 기준으로 df 합산
    merged_df = pd.concat([df3, ly_df2], ignore_index=True)

    result = merged_df.groupby('id')[['romantic', 'adventurous', 'depresed','powerful']].sum().reset_index()

    for i in range(result.shape[0]):
        #데이터 삽입
        insert_query = """
            INSERT INTO audio_features (f1, f2, f3, f4, track_id) values (%s, %s, %s, %s, %s);
        """
        id = df3.iloc[i]['track_id']
        cursor.executemany(insert_query, [(float(val)) if type(val)!=str else str(val) for val in df3.iloc[i].values])
        
        #is_analyze 업데이트
        flag_update_query = f"""
        UPDATE spotify_audio_features
        SET is_analyze = True
        WHERE id = {id};
        """
        cursor.execute(flag_update_query)
        
        
        conn.commit()


    cursor.close()
    conn.close()

