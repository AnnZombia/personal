import mysql.connector
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import auth_getphone as auth_getphone
import auth_getcode as auth_getcode
from random import random, randint

def main():
  api_id = 10787535
  api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'
  username = 'AnnZombia'
  uniq_key = randint (1000000000,9999999999)
  
  client = TelegramClient(username, api_id, api_hash)
  client.connect()

  mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Aksenov/1",
    database = "app"
    )
  
  if not client.is_user_authorized():
    cursor = mydb.cursor()
    auth_getphone.main(uniq_key)
    cursor.execute("SELECT phone FROM auth WHERE uniq = %s", (uniq_key,))
    record = cursor.fetchone()
    phone='+'+str(record[0])
    print(phone)
    client.send_code_request(phone)
    auth_getcode.main()
    cursor.execute("SELECT code FROM auth WHERE uniq = %s", (uniq_key,))
    record = cursor.fetchone()
    code = record[0]
    print(code)
    mydb.commit()
    cursor.close()
    mydb.close()
    
    try:
        client.sign_in(phone, code)
        print("sign by code")
    except SessionPasswordNeededError:
        client.sign_in(password)
    
    me = client.get_me()
    print(me)
   
main()
