from yandex_music import Client

#uid="annzombia"
TOKEN= 'AQAAAABh0mlaAAG8Xq0-0CDnOEUsiBThpsRaiqQ'
#TOKEN= 'AQAAAABhqZ3-AAG8XgFAmcE-Jk7UhWuPQndiQIE'
client = Client(TOKEN).init()
test = client.users_likes_tracks().fetch_tracks()
#print(test)
for i in len(test):
      for j in len(artists):
            print(test[i].artists[j]['name'],'\n')

