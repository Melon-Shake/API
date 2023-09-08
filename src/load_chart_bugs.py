import requests

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_bugs import BugsEntity

if __name__ == '__main__':

    _USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    _IMAGE_PREFIX_URL = "https://image.bugsm.co.kr/album/images"
    _CHART_API_URL = "https://m.bugs.co.kr/api/getChartTrack"

    headers = {
        "User-Agent": _USER_AGENT,
    }

    Domestic = 20152 # 국내차트 - 20152
    Realtime = 'realtime' # 시간별차트
    headers = {"User-Agent": _USER_AGENT}
    data = {"svc_type": Domestic, "period_tp": Realtime,"size":100,}
    response = requests.post(_CHART_API_URL, headers=headers, data=data)
    if response.status_code == 200 :
        responsed_data = response.json().get('list')
    
        for x in responsed_data :
            entity = BugsEntity(**x)
            # print(entity.track_id)
            # print(entity.track_title)
            # print(entity.album.album_id)
            # print(entity.album.title)
            # print(_IMAGE_PREFIX_URL+'/256'+entity.album.image.path)
            # print(entity.album.release_ymd)
            # print(entity.album.release_local_ymd)
            # print(entity.artists[0].artist_id)
            # print(entity.artists[0].artist_nm)
            # print(entity.artists[0].genres[0].svc_nm)
            # print(entity.adhoc_attr.likes_count)
            # print(entity.list_attr.rank)
            # print(entity.list_attr.rank_peak)
            print(entity.list_attr.rank_last)