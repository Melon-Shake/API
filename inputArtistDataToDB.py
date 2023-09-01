import requests
import lib.module as module
import string
import psycopg2
import config.db_info as db

conn = psycopg2.connect(**db.db_params)

access_token = module.read_AuthToken_from_file()

# test용
artist_id = '5dCvSnVduaFleCnyy98JMo'

url = f'https://api.spotify.com/v1/artists/{artist_id}'
header = {
    'Authorization': 'Bearer ' + access_token
}
response = requests.get(url, headers=header)
response_json = response.json()
print(response_json)

# sp_artist table 에 넣을 컬럼
external_urls = response_json['external_urls']['spotify']
# print(external_urls)
genres = response_json['genres']
href = response_json['href']
sp_artist_id = response_json['id']
images_url = response_json['images'][0]['url']
name = response_json['name']
popularity = response_json['popularity']
type = response_json['type']
uri = response_json['uri']

# artist 테이블
# art_id = '1'
name_org = response_json['name']
name_sub =''
image = response_json['images'][0]['url']

# # 커서
cur = conn.cursor()
query1 = "INSERT INTO sp_artist (external_urls,genres,href,id,images_url,name,popularity,type,uri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
query2 = "INSERT INTO artist ( name_org, name_sub, image) VALUES(%s,%s,%s)"
cur.execute(query1, (external_urls,genres,href,sp_artist_id,images_url,name,popularity,type,uri))
cur.execute(query2, (name_org,name_sub,image))
# # 커밋 및 연결 닫기
conn.commit()
cur.close()
conn.close()










