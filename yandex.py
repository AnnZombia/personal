from yandex_music import Client

#uid="annzombia"
uid=389169

client = Client().init()
test = client.users_likes_tracks(user_id=uid)[0].fetch_track()

print(test)
