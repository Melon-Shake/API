from fastapi import FastAPI
import requests
import module
from pydantic import BaseModel
app = FastAPI()

access_token = module.read_AuthToken_from_file()

class SearchKeyword(BaseModel):
    searchInput : str

@app.post("/search/")
def search_spotify(data:SearchKeyword):
    q = data.searchInput
    url = f'https://api.spotify.com/v1/search?q={q}&type=album%2Cartist%2Ctrack&market=kr'
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return_data ={}
        for i in range(len(response_json["tracks"]["items"])):
            list_artist = []
            for j in range(len(response_json["tracks"]["items"][i]["artists"])):
                list_artist.append(response_json["tracks"]["items"][i]["artists"][j]["name"])
            return_data["tracks"+str(i)]=[[response_json["tracks"]["items"][i]["name"]],
                            [response_json["tracks"]["items"][i]["album"]["name"]],
                            list_artist]                
        for i in range(len(response_json["albums"]["items"])):
            # print(response_json["albums"]["items"][i]["name"])
            return_data["albums"+str(i)]=[[response_json["albums"]["items"][i]["name"]]]
        for i in range(len(response_json["artists"]["items"])):
            # print(response_json["artists"]["items"][i]["name"])
            return_data["artists"+str(i)]=[[response_json["artists"]["items"][i]["name"]]]
            # response_json["tracks"]["items"]["name"]
        # print(len(response_json))
        print(return_data)
        return return_data
    else:
        return {"error": "Spotify API request failed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
