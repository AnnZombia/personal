from yandex_music import Client

#uid="annzombia"

TOKEN= 'AQAAAABhqZ3-AAG8XgFAmcE-Jk7UhWuPQndiQIE'
client = Client(TOKEN).init()
test = client.users_likes_tracks()[1].fetch_track()

print(test.artists[0]['name'])
