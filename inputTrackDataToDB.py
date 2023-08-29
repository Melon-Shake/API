import requests
import module
import string
import psycopg2
import config.db_info as db

def has_non_english_characters(text):
    for char in text:
        if char not in string.printable or char in string.ascii_letters:
            return True
    return False

conn = psycopg2.connect(
    database = db.database,
    user = db.user,
    password = db.password,
    host = db.host,
    port = db.port
)

access_token = module.read_AuthToken_from_file()

track_id = '3rrYAxy6f1Aj5GO9vVRyDr'

url = f'https://api.spotify.com/v1/tracks/{track_id}?market=kr'
header = {
    'Authorization': 'Bearer ' + access_token
}
response = requests.get(url, headers=header)
response_json = response.json()

# sp_track table 에 넣을 컬럼
# available_markets = response_json['available_markets']
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
album_id =response_json['album']['id']
artist_id = response_json['artists'][0]['id']

# track
duration = response_json['duration_ms']/1000
genres = response_json
image = response_json['album']['images'][0]['url']
name_has = has_non_english_characters(response_json['name'])

if name_has != True:
    name_org = response_json['name']
    query2 = "INSERT INTO track (name_org, duration, image) VALUES(%s,%s,%s)"
    cur = conn.cursor()
    cur.execute(query2, (name_org, duration, image))
    # 커밋 및 연결 닫기
    conn.commit()
    cur.close()
    conn.close()
        
else:
    name_org = response_json['name']
    name_eng = response_json['name']
    query2 = "INSERT INTO track (name_org, name_eng, duration, image, id) VALUES(%s,%s,%s,%s)"
    cur = conn.cursor()
    cur.execute(query2, (name_org, name_eng, duration, image))

    # 커밋 및 연결 닫기
    conn.commit()
    cur.close()
    conn.close()

# 커서
cur = conn.cursor()
query1 = "INSERT INTO sp_track (disc_number, duration_ms, explicit, external_urls, href, id, is_playable, name, popularity, preview_url, track_number, type, uri, is_local, album_id, artist_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
cur.execute(query1, (disc_number,duration_ms,explicit,external_urls,href,id,is_playable,name,popularity,preview_url,track_number,type,uri,is_local,album_id,artist_id))
# 커밋 및 연결 닫기
conn.commit()
cur.close()
conn.close()










