import requests as rq
import json
from secrets import SPOTIFY_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_SEARCH
from refresh_spotify import refresh_token


SPOTIFY_CREATE_PLAYLIST_URL = 'https://api.spotify.com/v1/users/{}/playlists'.format(SPOTIFY_CLIENT_ID)
random_pl_id_to_test = "6cfGDW3P18CNllLr4hFIVb"
random_list_to_test = []

for i in range(203):
    random_list_to_test.append(i)

playlist_id = ""
testplid = "3r8blOHBHTzFpiZEkgZCa3"
testurilist = ['spotify:track:7ycWLEP1GsNjVvcjawXz3z', 'spotify:track:18pwD0HrweX8oCgIkayRb4', 'spotify:track:2hyF1YWdX8yxExvRelT9nB', 'spotify:track:5Z8HZM6iQMhhqyPcCGY5g9', 'spotify:track:3pndPhlQWjuSoXhcIIdBjv', 'spotify:track:1ZAyjvIk9YiD76yYy0TEG6', 'spotify:track:7sO5G9EABYOXQKNPNiE9NR', 'spotify:track:2t8yVaLvJ0RenpXUIAC52d', 'spotify:track:2fQrGHiQOvpL9UgPvtYy6G', 'spotify:track:1lOe9qE0vR9zwWQAOk6CoO', 'spotify:track:1fEl5TPKRJAsuP6TqZ23hB', 'spotify:track:1rsAFUCa6BVMgRQ3FCQQsi', 'spotify:track:1GeNui6m825V8jP4uKiIaH', 'spotify:track:5ry2OE6R2zPQFDO85XkgRb', 'spotify:track:1e1JKLEDKP7hEQzJfNAgPl', 'spotify:track:4Km5HrUvYTaSUfiSGPJeQR', 'spotify:track:5BJMeoCXXgbRAWfp6fTulr', 'spotify:track:2zjGJ0dChMR0KxBZS15aqo', 'spotify:track:4sjiIpEv617LDXaidKioOI', 'spotify:track:2QgfDF0fQ4sskDthP8MG5w', 'spotify:track:4IO8X9W69dIQe0EC5ALXhq', 'spotify:track:1vc2YF7ZvUtwr45HNpdGch', 'spotify:track:1nO2NjuFkGaAWcMdJ1pNrp', 'spotify:track:1xzBco0xcoJEDXktl7Jxrr', 'spotify:track:0DWrG09StYVhLbeNLwAJ5w', 'spotify:track:2FoRvrNWBtrJiSgIjmivKG', 'spotify:track:6uFn47ACjqYkc0jADwEdj1', 'spotify:track:3RZftiuTcLOqpsd8ZlwNhr', 'spotify:track:2aV5ZEAvHwvL332EsJ1gWc', 'spotify:track:2cWCuKoUEw7u75hHyN5A33', 'spotify:track:62vpWI1CHwFy7tMIcSStl8', 'spotify:track:225I92Od6UNxwRJx9rUiyV', 'spotify:track:0nbXyq5TXYPCO7pr3N8S4I', 'spotify:track:6gi6y1xwmVszDWkUqab1qw', 'spotify:track:5uwf43E8QHEcDONhf8EI27', 'spotify:track:79s5XnCN4TJKTVMSmOx8Ep', 'spotify:track:3yOlyBJuViE2YSGn3nVE1K', 'spotify:track:69fnnbeoZO9h16CUZGIbTG', 'spotify:track:4PklAHGXT5ityno3IA8SKd', 'spotify:track:6cr5ajjgxZ8pnIJrGyLaTX', 'spotify:track:5NHIlHQZvm0k52AhBusT1R', 'spotify:track:7wsmIIm0xWmtP7TmACXkJn', 'spotify:track:7GwYENSg87oERcW0Wacd6m', 'spotify:track:3SEd8nPd8MpGwk6ZZ8tk2j']

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
    # print(json_response)
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
        uri_list.reverse()
        for x in range(test + 1):
            i = 0
            while len(uri_list) > 0 and i != 100:
                item_to_add = uri_list.pop()
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

    # print(json_response)




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
        test_list = uri_list
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

            print(naujas)

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

#
# clear_playlist(random_pl_id_to_test, random_list_to_test)