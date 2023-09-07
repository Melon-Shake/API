import requests
import sys
from model.flo_db import FloEntity

if __name__ == '__main__':

    response = requests.get("https://api.music-flo.com/display/v1/browser/chart/1/list?mixYn=N"
                      ,headers = {"User-Agent": "okhttp/4.9.2",
                                  "x-gm-app-name":"FLO",
                                   "x-gm-app-version": ""
                                }
                      )

    if response.status_code == 200 :
        responsed_data = response.json().get('data').get('trackList')
        #print(responsed_data[0].get('trackTitle'))
        #print(type(responsed_data.get('data').get('trackList')[0].get('id')))
        for x in responsed_data :
            entity = FloEntity(**x)
            print(entity)
      