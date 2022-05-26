from yandex_music import Client
client = Client().init()

test =  client.usersLikesTracks('axl.and')
print(test)
