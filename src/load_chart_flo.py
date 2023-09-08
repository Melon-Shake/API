import requests

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_flo import ChartFlo, ChartFloORM
from model.database import session_scope

if __name__ == '__main__':

    response = requests.get("https://api.music-flo.com/display/v1/browser/chart/1/list?mixYn=N"
                      ,headers = {"User-Agent": "okhttp/4.9.2",
                                  "x-gm-app-name":"FLO",
                                   "x-gm-app-version": ""
                                }
                      )

    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = responsed_data.get('data').get('trackList')

        from model.flo_db import FloChart, FloArtist, FloAlbum, FloTrack

        # parsed_data.reverse()
        for i, e in enumerate(parsed_data) :
            entity = ChartFlo(**e)
            
            track_orm = FloTrack(id=entity.id, name=entity.name)
            print(track_orm.name)
            album_orm = FloAlbum(entity.album)
            print(album_orm.title)
            artist_orm = FloArtist(entity.representationArtist)
            print(artist_orm.name)

            chart_orm = FloChart(index=i, artist=artist_orm, album=album_orm, track=track_orm)
            print(chart_orm.id)
            print(chart_orm.rank)
            print(chart_orm.points)
            print(chart_orm.artist)
            print(chart_orm.album)
            print(chart_orm.track)

            with session_scope() as session :
                session.add(chart_orm)
            