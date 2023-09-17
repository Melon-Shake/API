from model.jun_model import search_track
import psycopg2
from config.db_info import db_params

def pick_data(data: search_track,db_params):
    email = data.email
    track_title = data.track_title

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()
    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None

    track_search = "SELECT id from spotify_tracks where name = %s"
    track_value = (track_title,)
    cursor.execute(track_search, track_value)
    track_query_result = cursor.fetchone()
    if user_query_result:
        track_id = track_query_result[0]

    search_query = "INSERT INTO search_log_tracks(spotify_tracks_id,user_id) values (%s,%s);"
    user_values = (track_id, user_id)
    cursor.execute(search_query, user_values)
    connection.commit()
    cursor.close()
    connection.close()
