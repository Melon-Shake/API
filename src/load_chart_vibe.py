import requests

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_vibe import VibeEntity, VibeORM
from model.database import session_scope

if __name__ == '__main__':

    _USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    _ACCEPT = "application/json"
    _CHART_API_URL = "https://apis.naver.com/vibeWeb/musicapiweb/vibe/v1/chart/track/total"

    headers = {
        "User-Agent": _USER_AGENT,
        "Accept": _ACCEPT
    }

    queryStart = int(1)
    queryCount = int(100)
    
    response = requests.get(
        f"{_CHART_API_URL}?start={queryStart}&display={queryCount}",
        headers=headers
    )

    if response.status_code == 200 :
        responsed_data = response.json().get('response').get('result').get('chart').get('items').get('tracks')

        entries = {}
        for itme in responsed_data:
            for index, item in enumerate(responsed_data):
                track_title = item['trackTitle']
                artists = item.get('artists')
                artist_pre = []
                for artist in artists:
                    artist_nm = artist['artistName']
                    artist_pre.append(artist_nm)
                entries[index+1] = [track_title, artist_pre]
        # for x in responsed_data :
        #     entity = VibeEntity(**x)
        #     orm = VibeORM(entity)

        #     with session_scope() as session :
        #         session.add(orm)