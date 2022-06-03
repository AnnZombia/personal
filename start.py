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
uid = 'axl.and'
TOKEN= 'AQAAAAAzeKyBAAG8Xv5pPqRMI0UVnRIkA9VYDos'
status = 0
last_version = list()
new_version = list()


client_mus = Client(TOKEN).init()

with TelegramClient('/home/centos/bot/AnnZombia.session', api_id, api_hash) as client:
    while True:
          tracks = client_mus.users_likes_tracks(uid).fetch_tracks()      
          client.connect()
	
          for i in range(len(tracks)):
                for j in range(len(tracks[i].artists)):
                      track = tracks[i].artists[j]['name']+'-'+tracks[i].title
                      new_version.append(track)

          diff_del = list(set(last_version) - set(new_version))
          diff_add = list(set(new_version) - set(last_version))
          diff = list(set(last_version) ^ set(new_version))
          message_del = 'deleted track: ' + str(diff_del)
          message_add = 'added track: ' + str(diff_add)
          if diff:
                if diff_del:
                      client.send_message('AnnZombia2', message_del)
                elif diff_add and status != 0:
                          client.send_message('AnnZombia2', message_add)
			
          last_version = list(new_version)
          new_version = list()
          client.disconnect()
          status = 1
          time.sleep(5)

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
