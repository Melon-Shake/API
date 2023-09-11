# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # with open('config/client_secret_CLIENTID.json', 'r') as file :
    #     client_secrets_file = json.load(file)
    # str_file = json.dumps(client_secrets_file)

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
     "config/client_secret_CLIENTID.json", scopes)
    
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet, contentDetails",
        maxResults=100,
        #한국 인기 top100 플레이리스트
        playlistId="PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()