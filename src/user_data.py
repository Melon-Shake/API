from model.jun_model import LoginData
from config.db_info import db_params
import psycopg2
from datetime import datetime
import bcrypt


def user_data(data: LoginData,db_params):
    email = data.email
    password = data.password
    gender = data.gender
    birthdate = datetime.strptime(data.birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    mbti = data.mbti
    favorite_tracks = data.favorite_tracks
    favorite_artists = data.favorite_artists
    name = data.name
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    # 패스워드 해싱
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # INSERT 쿼리 실행
    user_query = "INSERT INTO \"user\"(password,email,name) values (%s, %s,%s) RETURNING id;"

    user_values = (hashed_password.decode("utf-8"),email,name)

    cursor.execute(user_query, user_values)
    user_detail_query = "INSERT INTO user_properties(gender,age,mbti,favorite_tracks,favorite_artists,user_id) values (%s,%s,%s,%s,%s,%s)"
    try:
        user_query_id = cursor.fetchone()[0]
        user_detail_values= (gender,age,mbti,favorite_tracks,favorite_artists,user_query_id)
        cursor.execute(user_detail_query,user_detail_values)
        connection.commit()
        cursor.close()
        connection.close()
    except (psycopg2.IntegrityError, psycopg2.Error) as e:
        if "duplicate key value violates unique constraint" in str(e):
            print("이미 등록된 Email 입니다.")
            return "이미 등록된 Email 입니다."
        else:
            print("다른 예외 발생:", e)
            return "다른 예외 발생"


