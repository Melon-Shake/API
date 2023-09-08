import requests
import config.youtubekey as youtube
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.ytmusic import js_ChartYoutube, js_SumChart

key= youtube.key

url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2C%20contentDetails&maxResults=100&playlistId=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&key={key}'

response = requests.get(url)

if response.status_code == 200:
    response_json = response.json()
    next_page_token = response_json['nextPageToken']
    # print(next_page_token)
    playlist_item = response_json.get('items')
    youtube_args1 = []
    # print(type(playlist_item[0]['contentDetails']['videoPublishedAt']))
    for item in playlist_item : 
        youtube_item = js_ChartYoutube(**item)
        # print(youtube_item)
        youtube_args1.append(youtube_item)
        
        
    url2 = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2C%20contentDetails&maxResults=100&pageToken={next_page_token}&playlistId=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&key={key}'
    response2 = requests.get(url2)
    
    response2_json = response2.json()
    playlist_item2 = response2_json.get('items')
    
    youtube_args2 = []
    for item2 in playlist_item2:
        # print(item2.get('contentDetails'))
        youtube_item2 = js_ChartYoutube(**item2)
        youtube_args2.append(youtube_item2)
        # print(youtube_item2)
        # print(type(youtube_item2))
else:
    print('error_code ='+ response.status_code)

result_item = youtube_args1+youtube_args2
result_chart = js_SumChart(result_item=result_item)
print(result_chart)

# print(playlist_item2[0]['contentDetails'])
#     for i in range(len(response_json['items'])):
#         playlist_item['rank'+ str(i)] = [response_json['items'][i]['snippet']['position'],
#                                         response_json['items'][i]['snippet']['title'],
#                                         response_json['items'][i]['snippet']['description'],
#                                         response_json['items'][i]['snippet']['thumbnails']['default']['url'],
#                                         response_json['items'][i]['contentDetails']['videoPublishedAt']
#                                             ]
#     print(playlist_item)


