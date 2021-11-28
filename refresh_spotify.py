import requests
from secrets import CLIENT_ID, CLIENT_SECRET, SPOTIFY_CLIENT_ID, REDIRECT_URI
import base64
import json
from spotipy.oauth2 import SpotifyOAuth
import webbrowser


SPOTIFY_CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/{}/playlists'.format(SPOTIFY_CLIENT_ID)

authURL = 'https://accounts.spotify.com/api/token'

authHeader = {}

authData = {}
def refresh_token():
    message = f"{CLIENT_ID}:{CLIENT_SECRET}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    # print(base64_message)
    authHeader['Authorization'] = f"Basic {base64_message}"
    authData['grant_type']= 'client_credentials'

    response = requests.post(authURL, headers=authHeader, data=authData)

    access_token = response.json()['access_token']

    # print(access_token)
    return access_token


# a = refresh_token()

def user_auth():
    auth_link =    f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scopes=playlist-modify-public"
    # response = requests.get(auth_link)

    webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser(
                            "C://Program Files//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open_new(auth_link)


# user_auth()