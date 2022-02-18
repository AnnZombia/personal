import mysql.connector
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import auth_getphone as auth_getphone
import auth_getcode as auth_getcode
from random import random, randint

def main():
  api_id = 10787535
  api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'
  uniq_key = randint (1000000000,9999999999)
  
  mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Aksenov/1",
    database = "app",
    get_warnings = True
    )

# need to write additional function for user_id retrieving
  client = TelegramClient('AnnZombia', api_id, api_hash)
  client.connect()  
  
# authorization check
  if not client.is_user_authorized():
    cursor = mydb.cursor()
    
# get phone number and write it to DB
    auth_getphone.main(uniq_key)
    cursor.execute("SELECT phone FROM auth WHERE uniq = %s", (uniq_key,))
    record = cursor.fetchone()
    phone='+'+str(record[0])

# send code to client phone
    client.send_code_request(phone)
  
    
# get code and write it to DB
    auth_getcode.main(uniq_key)
    cursor.execute("SELECT code FROM auth WHERE uniq = %s", (uniq_key,))
    record = cursor.fetchone()
    code = record[0]
    mydb.commit()

    
    try:
        client.sign_in(phone, code)
        print("sign by code")
    except SessionPasswordNeededError:
        client.sign_in(password) # need to write additional function for password retrieving
    
    me = client.get_me()
    if client.get_me().first_name != None:
      cursor.execute("DELETE FROM auth WHERE uniq = %s", (uniq_key,))
      mydb.commit()
      cursor.close()
      mydb.close()
    print(client.get_me().first_name)
     
main()
