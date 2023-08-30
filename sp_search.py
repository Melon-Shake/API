from fastapi import FastAPI
import requests
import module

app = FastAPI()

access_token = module.read_AuthToken_from_file()

# curl --request GET \
#   --url 'https://api.spotify.com/v1/search?q=%EC%A2%8B%EC%9D%80%EB%82%A0&type=album%2Cartist%2Ctrack&limit=3' \
#   --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'

@app.post("/search")
def search_spotify(q: str):
    url = f'https://api.spotify.com/v1/search?q={q}&type=album%2Cartist%2Ctrack&market=kr'
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    response_json = response.json()
    return response_json    # else:
        # return {"error": "Spotify API request failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
