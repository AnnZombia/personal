import mysql.connector
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import auth_getphone as auth_getphone
from random import random, randint

def main():
  api_id = 10787535
  api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'
  username = 'AnnZombia'
  uniq_key = randint (1000000000,9999999999)
  
  client = TelegramClient(username, api_id, api_hash)
  client.connect()

  auth_getphone.main(uniq_key)
  mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Aksenov/1",
    database = "app"
    )
  
  if not client.is_user_authorized():
    cursor = mydb.cursor()
    auth_getphone.main(uniq_key)
    phone = cursor.execute("SELECT phone FROM auth WHERE uniq = %s", (uniq_key,))
    client.send_code_request(phone)
    auth_code.main()
    code = cursor.execute("SELECT code FROM auth WHERE uniq = %s", (uniq_key,))
    mydb.commit()
    cursor.close()
    mydb.close()
    
    try:
        client.sign_in(phone, code)
    except SessionPasswordNeededError:
        client.sign_in(password)
    
    me = client.get_me()
    print(me)
