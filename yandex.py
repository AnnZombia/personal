#from yandex_music import Client


#test = client.users_likes_tracks(kind=kind, user_id=863546497).fetch_tracks()
#test = client.users_likes_tracks(user_id="annzombia")[0].fetch_track()
#print(test)

from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject, Client, Account, Permissions, Subscription, Plus, StationData, Alert, Status
from yandex_music.utils import model
#status = Status('annzombia','read')



TOKEN= 'AQAAAABh0mlaAAG8Xq0-0CDnOEUsiBThpsRaiqQ'
client = Client(TOKEN).init()


perm = Permissions('','','')

permi = perm.de_json(data: 'values', client: 'annzombia')
print(permi)
