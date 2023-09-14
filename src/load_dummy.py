import pandas as pd
import psycopg2
from config.db_info import db_params

gpt_data = pd.read_csv("C:/Users/eagls/chatgpt1.csv")
a = gpt_data.dropna(subset=['hashtag', 'Username', 'Datetime'])

top_values = a['hashtag'].value_counts().head(5)

filtered_data = a[a['hashtag'].isin(top_values.index)]
id_count = filtered_data['Username'].nunique()

selected_columns = filtered_data[['Username', 'hashtag','Datetime']]

value_to_song = {'[]':"안녕",
                 "['#ChatGPT']":"Beautiful Pain",
                 "['#chatgpt']":"Bingo (ASSA)",
                 "['#chatGPT']":"Feel My Rhythm",
                 "['#ChatGPT', '#AI']":"Adios"}
selected_columns['hashtag'] = selected_columns['hashtag'].map(value_to_song)

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# 사용자 user table에 넣기 

for index, row in selected_columns.iterrows():
    password = index
    email = row['Username'] + '@play.com'
    insert_query = f'INSERT INTO "user" (password, email, name) VALUES (%s, %s, %s);'

    # 중복 확인을 위해 SELECT 쿼리 실행
    select_query = f'SELECT id FROM "user" WHERE email = %s;'
    cursor.execute(select_query, (email,))

    existing_record = cursor.fetchone()

    # 중복 레코드가 없을 때만 INSERT 실행
    if existing_record is None:
        try:
            cursor.execute(insert_query, (password, email, row['Username']))
            conn.commit()  # 커밋
        except psycopg2.Error as e:
            print("에러 발생:", e)
            conn.rollback()  # 롤백
    else:
        print(f"중복 레코드 발견: {email}")

#search table에 노래와 사용자 email과 곡 데이터베이스 확인 후 id값 적재

for index, row in selected_columns.iterrows():
    email = row['Username'] + '@play.com'
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()
    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None
    track_title = row['hashtag']
    track_search = "SELECT id from track where name_org = %s"
    track_value = (track_title,)
    cursor.execute(track_search, track_value)
    track_query_result = cursor.fetchone()
    if user_query_result:
        track_id = track_query_result[0]
    
    datetime = row['Datetime']

    search_query = "INSERT INTO search_log_tracks(created_datetime,track_id,user_id) values (%s,%s,%s);"
    user_values = (datetime,track_id, user_id)
    cursor.execute(search_query, user_values)
    conn.commit()  # 커밋
