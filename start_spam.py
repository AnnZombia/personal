import os
import datetime
from telethon import TelegramClient, events, sync
import random

api_id = 10787535 
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'

user='@'+'unitedcatsupport'

with TelegramClient('/home/centos/bot/AnnZombia2.session', api_id, api_hash) as client:
    while True:
          time = datetime.datetime.now()
          if time.hour == 9:
#if time.hour == 9 and time.minute == 0:
              client.connect()
              with open ('phrases.txt', 'r') as file:
                  lines = file.readlines()
                  print(random.choice(lines))
                  client.send_message(user, random.choice(lines))
               
              client.disconnect()
              time.sleep(60)
