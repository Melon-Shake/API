import requests
import module
import string
import psycopg2
import psycopg2
import requests
import json
from urllib.parse import quote
# from config.info import *   
import base64

def create_access_token():
    client_id = "1180fb31cb794ef887bb18daa3eccd90"
    client_secret = "e1e314e15fa84210bb4cebd6cc13a0d5"

    Refresh_token = module.read_RefreshToken_from_file()

    url = "https://accounts.spotify.com/api/token"
    header = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
        }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": Refresh_token 
    }

    response = requests.post(url,headers=header,data=data)

    response_json = response.json()
    access_token=response_json["access_token"]
    with open("config/AuthToken.txt", "w") as file:
            file.write(access_token)
    access_token = module.read_AuthToken_from_file()
    return access_token
        
def get_sp_track_id(artist, album, track):
    
    access_token = create_access_token()
    con = psycopg2.connect(
            user="postgres",
            password="12345678",
            host="database-1.coea55uwjt5p.ap-northeast-1.rds.amazonaws.com",
            port="5432",
            database="postgres"
        )

    cur = con.cursor()

    # query = 'select track_name, album_name, artist_name from route where True'
    query = f"""SELECT id
                FROM route
                WHERE artist_name = '{artist}'
                    AND album_name = '{album}'
                    AND track_name = '{track}';
                """
    cur.execute(query)

    res = cur.fetchone()
    # return res
    
    if res: # 라우트에 적제되어있을때
        route_id = res[0]
        url = f'https://api.spotify.com/v1/search?q={track}%2C+{artist}%2C+{album}&type=track&limit=3'
        header = {
            'Authorization': 'Bearer ' + access_token 
        }
        response = requests.get(url=url,headers=header)
        response_json = response.json()
        
        items = response_json.get('tracks').get('items')
        con.commit()
        cur.close()
        con.close()
    else: # 적재되어있지 않으면 재귀
        query = f"INSERT INTO route (track_name, album_name, artist_name) VALUES ('{track}', '{album}', '{artist}') RETURNING id"
        cur.execute(query)
        route_id = cur.fetchone()[0]
        url = f'https://api.spotify.com/v1/search?q={track}%2C+{artist}%2C+{album}&type=track&limit=3'
        header = {
            'Authorization': 'Bearer ' + access_token 
        }
        response = requests.get(url=url,headers=header)
        response_json = response.json()
        items = response_json.get('tracks').get('items')
        
        con.commit()
        cur.close()
        con.close()
        print(f'데이터 적재 후 재실행')
        # get_sp_track_id(artist, album, track)
        
        
    
    for item in items :
        tracks = item.get('name')
        albums = item.get('album').get('name')
        artists = item.get('artists')[0].get('name')
        if track == tracks:
            if album == albums:
                if quote(artist) == artists:
                    return(item.get('id'), route_id)
                else:
                    return ((artist,artists),(album,albums),(track,tracks))
            else:
                return ('b','c')
        else:
            return ('c','d')






def has_non_english_characters(text):
    for char in text:
        if char not in string.printable or char in string.ascii_letters:
            return True
    return False


def sp_and_track_input(track_id,route_id):
    sp_input_result = {}
    
    try:
        sp_input_result['track_id'] = track_id
        
        conn = psycopg2.connect(
            user="postgres",
            password="12345678",
            host="database-1.coea55uwjt5p.ap-northeast-1.rds.amazonaws.com",
            port="5432",
            database="postgres"
        )
        
        with conn:
            with conn.cursor() as cur:
                access_token = create_access_token()

                url = f'https://api.spotify.com/v1/tracks/{track_id}?market=kr'
                header = {
                    'Authorization': 'Bearer ' + access_token
                }
                response = requests.get(url, headers=header)
                response_json = response.json()

                disc_number = response_json['disc_number']
                duration_ms = response_json['duration_ms']
                explicit = response_json['explicit']
                external_urls = response_json['external_urls']['spotify']
                href = response_json['href']
                id = response_json['id']
                is_playable = response_json['is_playable']
                name = response_json['name']
                popularity = response_json['popularity']
                preview_url = response_json['preview_url']
                track_number = response_json['track_number']
                type = response_json['type']
                uri = response_json['uri']
                is_local = response_json['is_local']
                album_id = response_json['album']['id']
                artist_id = response_json['artists'][0]['id']

                duration = response_json['duration_ms'] / 1000
                image = response_json['album']['images'][0]['url']
                
                # 데이터베이스에 삽입
                query2 = "INSERT INTO track (name_org, duration, image) VALUES (%s, %s, %s)"
                if has_non_english_characters(name):
                    query2 = "INSERT INTO track (name_org, name_eng, duration, image, id) VALUES (%s, %s, %s, %s, %s)"
                    cur.execute(query2, (name, name, duration, image, route_id))
                else:
                    cur.execute(query2, (name, duration, image))

                query1 = "INSERT INTO sp_track (disc_number, duration_ms, explicit, external_urls, href, id, is_playable, name, popularity, preview_url, track_number, type, uri, is_local, album_id, artist_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query1, (
                    disc_number, duration_ms, explicit, external_urls, href, id, is_playable, name, popularity, preview_url, track_number,
                    type, uri, is_local, album_id, artist_id))

        sp_input_result['SP_track_input'] = 'SP_track_insert_good'
        
    except (Exception, psycopg2.Error) as error:
        sp_input_result['sp_input_except_err'] = str(error)
        
    finally:
        if conn:
            conn.close()
        url = "http://localhost:8000/lyric_input/"  

        data = {
            "artist": "(G)I-DLE",
            "track": "All Night",
            "track_id": track_id,
            "GENIUS_API_KEY" : "hvNyikfbrRz7IrjRN2wyrFwCc2YstwyCSsxcUAiwg9hbat_vNaEk8nqMBguxrlNt"
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            print(result)
        else:
            print("Request failed with status code:", response.status_code)
            print(response.text)
    return sp_input_result