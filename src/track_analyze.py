import psycopg2
import pandas as pd


def normalize_rows(df):
    # 데이터 프레임의 각 행을 정규화합니다.
    normalized_df = df.copy()
    for index, row in df.iterrows():
        # 행의 최솟값과 최댓값을 계산합니다.
        min_val = row.min()
        max_val = row.max()
        # 최솟값과 최댓값을 사용하여 행을 정규화합니다.
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
               select * from sp_audio_features
""")

# 결과 가져오기
column_info = cursor.fetchall()
column_info = [float(column_info[0][i]) if column_info[0][i] is not None else None for i in range(len(column_info[0])-2)]
print(column_info)
cursor.close()
conn.close()


column_info2 = column_info , column_info
columns = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
df = pd.DataFrame(column_info2, columns=columns)
df['tempo']= df['tempo']/60

df2 = normalize_rows(df)

df3 = pd.DataFrame()
df3['romantic'] = (df2['acousticness'] + df2['valence']) / 2
df3['adventurous'] =( df2['danceability'] + df2['tempo'])/2
df3['Melancholic'] = (1 - df2['energy']) * (1 - df2['loudness'])
df3['Powerful'] =  (df2['energy'] + (1 - df2['instrumentalness'])) / 2