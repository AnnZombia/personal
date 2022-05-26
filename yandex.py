from yandex_music import Client
client = Client().init()

test = client.tracks_list.TracksList(849346658).fetch_tracks()

print(test)
