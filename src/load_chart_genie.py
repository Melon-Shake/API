import requests

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_genie import ChartGenie

if __name__ == '__main__' :
    response = requests.post('https://app.genie.co.kr/chart/j_RealTimeRankSongList.json'
                             ,headers={
                                 'Content_Type' : 'application/x-www-form-urlencoded'
                             }
                             ,data={
                                 'dict': 'R'
                                 ,'pg_size': '200'
                             }
                            )

    if response.status_code == 200 :
        # print(response.status_code)
        # responsed_data = response.json()
        responsed_data = response.json().get('DataSet').get('DATA')
        # print(responsed_data)
        # print(type(responsed_data))
        # print(len(responsed_data))
        # print(responsed_data[0])

        for x in responsed_data :
            entity = ChartGenie(**x)
            # print(type(entity))
            print(entity.SONG_ID)
            print(entity.SONG_NAME)

    else : print(response.status_code)