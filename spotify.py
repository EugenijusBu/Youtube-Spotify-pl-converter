import requests as rq
import json
from secrets import SPOTIFY_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_SEARCH
from refresh_spotify import refresh_token


SPOTIFY_CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/{}/playlists'.format(SPOTIFY_CLIENT_ID)
playlist_id = ""

def create_playlist(name, public=True):
    response = rq.post(SPOTIFY_CREATE_PLAYLIST_URL,
                       headers = {"Authorization": f"Bearer {SPOTIFY_SECRET}"},
                       json= {
                           "name": name,
                           "public": public
                       }
                       )
    json_response = response.json()
    playlist_id = json_response["id"]

    print("Playlist created: " + name)
    print("Playlist id : " + playlist_id)
    return playlist_id

def search_song(song_name, artist):
    token = refresh_token()
    SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(song_name, artist)
    response = rq.get(SPOTIFY_SEARCH_URL,
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
                      )
    json_response = response.json()
    song = json_response["tracks"]["items"]

    try:
        uri = song[0]["uri"]
    except IndexError:
        uri = ""

    print(uri)
    return uri


def add_song(*, playlistid=playlist_id, uri_list):

    if len(uri_list)<=100:
        SPOTIFY_ADD_TO_PLAYLIST = "	https://api.spotify.com/v1/playlists/{}/tracks".format(playlistid)
        response = rq.post(SPOTIFY_ADD_TO_PLAYLIST,
                           headers={"Content-Type": "application/json", "Authorization": f"Bearer {SPOTIFY_SECRET}"},
                           json={
                               "uris": uri_list
                           }
                           )
        json_response = response.json()
    else:

        test = len(uri_list) // 100
        helper_list = []

        new_help_list = []

        new_help_list = uri_list.copy()
        new_help_list.reverse()
        for x in range(test + 1):
            i = 0
            while len(new_help_list) > 0 and i != 100:
                item_to_add = new_help_list.pop()
                helper_list.append(item_to_add)

                i += 1



            SPOTIFY_ADD_TO_PLAYLIST = "	https://api.spotify.com/v1/playlists/{}/tracks".format(playlistid)
            response = rq.post(SPOTIFY_ADD_TO_PLAYLIST,
                               headers={"Content-Type": "application/json",
                                        "Authorization": f"Bearer {SPOTIFY_SECRET}"},
                               json={
                                   "uris": helper_list
                               }
                               )
            print(response.json())
            helper_list.clear()





def clear_playlist(playlist_id, uri_list):

    if len(uri_list) <=100:
        print("I ran this code")
        naujas = []

        for item in uri_list:
            oneentry = {"uri": item}
            naujas.append(oneentry)



        SPOTIFY_CLEAR_PLAYLIST = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = rq.delete(SPOTIFY_CLEAR_PLAYLIST,
                             headers={"Content-Type": "application/json", "Authorization": f"Bearer {SPOTIFY_SECRET}"},
                             json={
                                 "tracks": naujas
                             })
        json_response = response.json()
        print(json_response)

    else:
        print("I else code")
        test_list = uri_list.copy()
        print(test_list)
        test = len(test_list) // 100
        print(test)

        for x in range(test + 1):
            i = 0
            helper_list = []
            while len(test_list) > 0 and i != 100:
                item_to_add = test_list.pop()
                helper_list.append(item_to_add)
                i += 1

            naujas_helper = []

            for item in helper_list:
                oneentry = {"uri": item}
                naujas_helper.append(oneentry)

            SPOTIFY_CLEAR_PLAYLIST = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            response = rq.delete(SPOTIFY_CLEAR_PLAYLIST,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {SPOTIFY_SECRET}"},
                                     json={
                                         "tracks": naujas_helper
                                     })
            json_response = response.json()
            print("playlistCleared")
            print(json_response)
