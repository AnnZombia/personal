from yandex_music import Client


client = Client().init()
test = client.users_likes_tracks('axl.and')



print(test)
