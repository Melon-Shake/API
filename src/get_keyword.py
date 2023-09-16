import psycopg2
from model.jun_model import Keyword
from config.db_info import db_params


def save_keyword_data(data: Keyword,db_params):
    keyword = data.searchInput
    email = data.email  # 사용자 이메일
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    # 등록한 이메일인 경우 ID 가져오기
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()
    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None
    search_query = "INSERT INTO search_log_keywords(keyword,user_id) values (%s,%s);"
    user_values = (keyword, user_id)
    cursor.execute(search_query, user_values)
    connection.commit()
    cursor.close()
    connection.close()