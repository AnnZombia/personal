from yandex_music import Client


#TOKEN= 'AQAAAABh0mlaAAG8Xq0-0CDnOEUsiBThpsRaiqQ'
#TOKEN= 'AQAAAABhqZ3-AAG8XgFAmcE-Jk7UhWuPQndiQIE'

client = Client().init()

#test = client.users_likes_tracks(user_id=1641179482).fetch_tracks()
#test = client.users_likes_tracks(user_id=1638505982).fetch_tracks()
test = client.users_likes_tracks().fetch_tracks()

print(test)

#for i in range(len(test)):
#      for j in range(len(test[i].artists)):
#            print(test[i].artists[j]['name'],'-', test[i].title)
