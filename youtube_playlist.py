import googleapiclient.discovery
import sched, time
from secrets import YT_DEV_KEY
import youtube_dl
from spotify import search_song, create_playlist, add_song, clear_playlist
import pafy

s = sched.scheduler(time.time, time.sleep)
playlist_id = "PLLeBzj9ZttfOcJ7o9XOeaqFs_Mv-RvpOz"

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = YT_DEV_KEY)

spotify_uris = []

playlist_item_ids = []

def get_playlist_name():
    request = youtube.playlists().list(
        part = "snippet",
        id = playlist_id
    )

    response = request.execute()
    title = response["items"][0]["snippet"]["title"]
    print(title)
    a = create_playlist(title)
    return a

idd = get_playlist_name()

def yt():
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)





    for item in range (len(playlist_items)):

        playlist_item_ids.append(playlist_items[item]["contentDetails"]["videoId"])


    print(f"total: {len(playlist_items)}")

    for item_id in playlist_item_ids:
        youtube_url = "https://www.youtube.com/watch?v={}".format(item_id)
        try:
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            try:
                song_name = video["track"]
                print(song_name)
                artist = video["artist"]
                print(artist)
                spotify_uri = search_song(song_name, artist)
                if spotify_uri != "":
                    spotify_uris.append(spotify_uri)

            except KeyError as e:
                print("Current song details unavailable")
        except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError) as e:
            pass

    add_song(uri_list=spotify_uris, playlistid=idd)
    print("All available songs were added successfully, in 60 seconds I will check for any changes! :)")
    s.enter(60, 1, do_something, (s,))
    s.run()


def do_something(sc):
    print("Checking for changes!")
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    check_playlist = []

    for item in range(len(playlist_items)):
        check_playlist.append(playlist_items[item]["contentDetails"]["videoId"])

    if check_playlist == playlist_item_ids:
        print("No changes made, i will check again in 60 seconds! :)")
    else:
        print("Oh no changes made to playlist, i will modify it!")
        clear_playlist(idd, spotify_uris)
        print(idd)
        print(spotify_uris)
        print(len(spotify_uris))
        time.sleep(10)
        playlist_item_ids.clear()

        for item in check_playlist:
            playlist_item_ids.append(item)

        spotify_uris.clear()

        for item_id in playlist_item_ids:
            youtube_url = "https://www.youtube.com/watch?v={}".format(item_id)
            try:
                video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
                try:
                    song_name = video["track"]
                    print(song_name)
                    artist = video["artist"]
                    print(artist)
                    spotify_uri = search_song(song_name, artist)
                    if spotify_uri != "":
                        spotify_uris.append(spotify_uri)

                except KeyError as e:
                    print("Current song details unavailable")
            except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError) as e:
                pass
        add_song(uri_list=spotify_uris, playlistid=idd)
        print("Playlist updated, enjoy your music, 60 seconds until i check again owo")
    s.enter(60, 1, do_something, (sc,))



yt()




