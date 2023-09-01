import requests
import module
import string
import psycopg2
import config.db_info as db

conn = psycopg2.connect(
    database = db.database,
    user = db.user,
    password = db.password,
    host = db.host,
    port = db.port
)

access_token = module.read_AuthToken_from_file()

album_id = '2cBuoAocFtOZU31Tk6UmTt'

url = f'https://api.spotify.com/v1/albums/{album_id}'
header = {
    'Authorization': 'Bearer ' + access_token
}
response = requests.get(url, headers=header)
response_json = response.json()
# sp_album table 에 넣을 컬럼
album_type = response_json['album_type']
total_tracks = response_json['total_tracks']
external_urls = response_json['external_urls']['spotify']
href = response_json['href']
sp_album_id = response_json['id']
images_url= response_json['images'][0]['url']
name = response_json['name']
release_date = response_json['release_date']
release_date_precision = response_json['release_date_precision']
# restrictions_reason =''
type = response_json['type']
uri = response_json['uri']
copyright_text = response_json['copyrights'][0]['text'] +" / "+ response_json['copyrights'][1]['text']
copyright_type = response_json['copyrights'][0]['type'] +" / "+ response_json['copyrights'][1]['type']
genres = response_json['genres']
label = response_json['label']
popularity = response_json['popularity']
artist_id = response_json['artists'][0]['id']

# album
id = '1'
name_has = module.has_non_english_characters(response_json['name'])
type = response_json['album_type']
tracks_cnt = response_json['total_tracks']
release_date = response_json['release_date']
image = response_json['images'][0]['url']
artist_id = '1'

with conn:
    with conn.cursor() as cur:
        if name_has != True:
            name_org = response_json['name']
            query2 = "INSERT INTO album (id,name_org, type, tracks_cnt,release_date,image,artist_id) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query2, (id,name_org,type,tracks_cnt,release_date,image,artist_id))         
        else:
            name_org = response_json['name']
            name_eng = response_json['name']
            query2 = "INSERT INTO album (id,name_org,name_eng, type, tracks_cnt,release_date,image,artist_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query2, (id,name_org,name_eng,type,tracks_cnt,release_date,image,artist_id))
        query1 = "INSERT INTO sp_album (album_type,total_tracks,external_urls,href,id,images_url,name,release_date,release_date_precision,type,uri,copyrights_text,copyrights_type,genres,label,popularity,artist_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query1, (album_type,total_tracks,external_urls,href,sp_album_id,images_url,name,release_date,release_date_precision,type,uri,copyright_text,copyright_type,genres,label,popularity,artist_id))
        
conn.close()










