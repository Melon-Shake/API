import bcrypt
import psycopg2
from model.jun_model import Login
from config.db_info import db_params

def authenticate_user(login_data: Login, db_params):  
    email = login_data.email
    password = login_data.password
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # 등록한 이메일인 경우 ID 가져오기
    user_query = "SELECT password FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()

    if user_query_result:
        condition = bcrypt.checkpw(password.encode("utf-8"), user_query_result[0].encode("utf-8"))
        cursor.close()
        if condition:
                # 패스워드가 일치하면 로그인 성공
                return True
        else:
            return False
