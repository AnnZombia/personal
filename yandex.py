from yandex_music import Client

uid='annzombia'

client = Client().init()
test = client.users_likes_tracks(user_id=uid)[0].fetch_track()

print(test)
