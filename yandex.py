from yandex_music import Client

TOKEN= 'AQAAAABh0mlaAAG8Xq0-0CDnOEUsiBThpsRaiqQ'
client = Client(TOKEN).init()
#test = client.users_likes_tracks(kind=kind, user_id=863546497).fetch_tracks()

test = client.users_likes_tracks(user_id="annzombia")[0].fetch_track()



print(test)
