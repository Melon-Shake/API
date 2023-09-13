import re, requests, sys, os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from update_token import return_token
from model.chart_vibe import VibeEntity, VibeORM
from model.database import session_scope

access_token = return_token()

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
        
        song_name = []
        artist_name = []
        album_name = []
        album_img = []

        entries = {}
        for index, item in enumerate(responsed_data):
            
            # 제목 디코딩
            pre_track_title = item['trackTitle']
            track_title = urllib.parse.unquote(pre_track_title)
            cleaned_track = re.sub(r'\([^)]*\)', '', track_title)
            
            # 예외 처리
            if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
                cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
                
            # 아티스트 디코딩
            pre_artist = item.get('artists')
            artist_pre = []
            
            for artist in pre_artist:
                artist_nm = artist['artistName']
                artists = urllib.parse.unquote(artist_nm)
                cleaned_artist = re.sub(r'\([^)]*\)', '', artists)
                artist_pre.append(cleaned_artist)
                
                if artist_nm == '#안녕':
                    artists = urllib.parse.quote(artist_nm)
                    
                artist_pre.append(artists)
            
            # 앨범 제목
            pre_album = item['album']['title']
            album = urllib.parse.unquote(pre_album)
            cleaned_album = re.sub(r'\([^)]*\)', '', album)

            artist_pre.append(artist_nm)
            entries[index] = [track_title, artist_pre, album_title]
        # for x in responsed_data :
        #     entity = VibeEntity(**x)
        #     orm = VibeORM(entity)

        #     with session_scope() as session :
        #         session.add(orm)