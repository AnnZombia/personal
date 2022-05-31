#from yandex_music import Client

client = Client('annzombia').init()
test = client.users_likes_tracks()[0].fetch_track()
print(test)
