import psycopg2
import config.database as db
import requests
import json

access_token = 'BQA_UVNeTW7JgezHC_Tti_nsJm6fmzFW2EeaS424k2xiSXl9SfNGq7jHdRlKq1oUXXmZML0mlM2Dj9iu57FhfkRA43JCM0io3nkNM5P0s9L0qi4pdgZNklXOJiDTNCHrvD_W9HrGrUTySlCdaH0vl8JfHK8JtXMIdvxoVkf5DFZj7XZ9pyaE3Nr-KObz9ONT5CppQd57Uw'

def get_track_id_from_spotify(track_name, album_name, artist_name) :
    url = f'https://api.spotify.com/v1/search?q={track_name}%2C+{artist_name}%2C+{album_name}&type=track&limit=3'
    header = {
        'Authorization': 'Bearer ' + access_token 
    }
    response = requests.get(url=url,headers=header)
    response_json = response.json()
    items = response_json.get('tracks').get('items')
    for idx, item in enumerate(items) :
        track = item.get('name')
        album = item.get('album').get('name')
        artist = item.get('artists')[0].get('name')
        if track == track_name :
            return item.get('id')

def insert_route(track_name, album_name, artist_name, cursor) :
    return 

def exists_route(track_name, album_name, artist_name, cursor) :
    query = f'''
        SELECT id FROM route
        WHERE (
            track_name = '{track_name}'
        AND album_name = '{album_name}'
        AND artist_name = '{artist_name}'
        )
    '''
    cursor.execute(query)
    if cursor.fetchone()[0] :
        return get_track_id_from_spotify(track_name, album_name, artist_name)
    else :
        insert_route(track_name, album_name, artist_name, cursor)

if __name__ == '__main__': 
    con = psycopg2.connect(
        database = db.DATABASE,
        user = db.USERNAME,
        password = db.PASSWORD,
        host = db.HOST,
        port = db.PORT
    )
    cur = con.cursor()

    track_name = 'All Night'
    album_name = 'I feel '
    artist_name = '(G)I-DLE'

    exists_route(track_name, album_name, artist_name, cur)

    con.commit()
    cur.close()
    con.close()