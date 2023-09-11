import requests
import lib.module as module
import string
import psycopg2
import config.db_info as db

conn = psycopg2.connect(**db.db_params)

access_token = module.read_AuthToken_from_file()

# test용
track_id = '5MvxeZPiiLAuB5gI8k3ynk'

# curl --request GET \
#   --url https://api.spotify.com/v1/audio-features/5MvxeZPiiLAuB5gI8k3ynk \
#   --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'

url = f'https://api.spotify.com/v1/audio-features/{track_id}'
header = {
    'Authorization': 'Bearer ' + access_token
}
response = requests.get(url, headers=header)
response_json = response.json()
print(response_json)
# # sp_audio_features table 에 넣을 컬럼
acousticness = response_json['acousticness']
danceability = response_json['danceability']
energy = response_json['energy']
instrumentalness = response_json['instrumentalness']
liveness = response_json['liveness']
loudness = response_json['loudness']
speechiness = response_json['speechiness']
valence = response_json['valence']
tempo = response_json['tempo']

with conn:
    with conn.cursor() as cur:
        query1 = "INSERT INTO sp_audio_features (acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query1, (acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo))
conn.close()










