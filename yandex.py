from yandex_music import Client

TOKEN= 'AQAAAABhqZ3-AAG8XgFAmcE-Jk7UhWuPQndiQIE'
client = Client(TOKEN).init()
test = client.users_likes_tracks(user_id=863546497).fetch_tracks()



print(test)
