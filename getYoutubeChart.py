from ytmusicapi import YTMusic
import config.youtubekey as youtube

yt = YTMusic('config/oauth.json')
playlistId = "PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m"
results = yt.get_charts('KR')
# seven = yt.search('Seven - Clean Ver. (feat. Latto)')
return_data = {}
print(results['songs']['items'][0])
# for i in range(len(results['songs']['items'])):
#     artist_list = []
#     for j in range(len(results["songs"]["items"][i]["artists"])):
#         artist_list.append(results["songs"]["items"][i]["artists"][j]["name"])
#     # 'album' 키가 있는지 확인하고 예외 처리 없는게 있음
#     album_name = results["songs"]["items"][i].get("album", {}).get("name", "Unknown Album")
#     return_data[str(i)]=[[results["songs"]["items"][i]["title"]],
#                          artist_list,
#                         [results["songs"]["items"][i]["thumbnails"][0]["url"]],
#                         album_name,
#                         [results["songs"]["items"][i]["rank"]]]
# print(return_data)

# curl \
#   'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails%2Cstatus%2Cid&maxResults=100&playlistId=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&key=[YOUR_API_KEY]' \
#   --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
#   --header 'Accept: application/json' \
#   --compressed

