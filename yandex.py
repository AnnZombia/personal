from yandex_music import Client
client = Client().init()

test = client.usersLikesTracks(849346658)[0].fetch_tracks()

print(test)
