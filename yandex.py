from yandex_music import Client

client = Client().init()
test = client.users_likes_tracks('annzombia')[0].fetch_track()
print(test)
