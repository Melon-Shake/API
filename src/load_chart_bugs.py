import requests

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_bugs import BugsEntity, BugsORM
from model.database import session_scope

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
        entries = {}
        for itme in responsed_data:
            for index, item in enumerate(responsed_data):
                track_title = item['track_title']
                album_title = item['album']['title']
                artists = item.get('artists')
                artist_pre = []
                for artist in artists:
                    artist_nm = artist['artist_nm']
                    artist_pre.append(artist_nm)
                entries[index+1] = [track_title, artist_pre, album_title]
        # {1: ['Smoke (Prod. Dynamicduo, Padi)', ['다이나믹 듀오', '이영지'], '스트릿 우먼 파이터2(SWF2) 계급미션'],}
        # for x in responsed_data :
        #     entity = BugsEntity(**x)
        #     orm = BugsORM(entity)

        #     with session_scope() as session :
        #         session.add(orm)