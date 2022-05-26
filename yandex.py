from yandex_music import Client


client = Client().init()
test = client.users_likes_tracks('axl.and')[0].fetch_track()
#test = client.usersLikesTracks(849346658)[0].fetch_tracks()

print(test)
