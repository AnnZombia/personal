from yandex_music import Client
import os
import time
from telethon import TelegramClient, events, sync
from telethon.tl.functions.users import GetFullUserRequest
import subprocess

api_id = 18598516 
api_hash = '3f866841c58e95685d8adda87e67a05a'
#client = TelegramClient('session_name', api_id, api_hash)
#client.start()

user='@'+'andreyaksenov'
uid = 'annzombia'
TOKEN= 'AQAAAAAzeKyBAAG8Xv5pPqRMI0UVnRIkA9VYDos'
status = 0
last_version = list()
new_version = list()


client = Client(TOKEN).init()


while True:
      tracks = client.users_likes_tracks(uid).fetch_tracks()

      for i in range(len(tracks)):
            for j in range(len(tracks[i].artists)):
		  track = tracks[i].artists[j]['name']+'-'+tracks[i].title
		  print(track)
                  new_version.append(track)
            
      diff = list(set(last_version + new_version))
      if diff == {}:
            print('нет разницы')
      else:
            if list(set(last_version) - set(new_version)) == {}:
                  print('удален трек')
            elif list(set(last_version) - set(new_version)) == {}:
                  print('добавлен трек')
      last_version = list(new_version)
      new_version = list()
      time.sleep(10)

#with TelegramClient('/home/centos/bot/AnnZombia.session', api_id, api_hash) as client:
#	while True:
#		client.connect()
#		full = client(GetFullUserRequest(user))
 #           tracks = client.users_likes_tracks(uid).fetch_tracks()
            
  #          for i in range(len(tracks)):
   #               for j in range(len(tracks[i].artists)):
			
    #                    new_version.append(tracks[i].artists[j]['name'],'-', tracks[i].title)
            
            
	#	if status != full.user.status:
	#		if full.user.status != None:
	#			client.send_message('AnnZombia2', 'Разблокировал в Телеграм')
	#		else:
	#			client.send_message('AnnZombia2', 'Заблокировал в Телеграм')
	#
	#	status = full.user.status
	#	client.disconnect()
	#	time.sleep(15)