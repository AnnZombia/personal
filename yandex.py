from yandex_music import Client

#uid="annzombia"
uid=1641179482
TOKEN= 'AQAAAABhqZ3-AAG8XgFAmcE-Jk7UhWuPQndiQIE'
client = Client(TOKEN).init()
test = client.users_likes_tracks(user_id=uid)[0].fetch_track()

print(test)
