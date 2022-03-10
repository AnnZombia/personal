import datetime
from telethon.tl.functions.users import GetFullUserRequest
import mysql.connector
import threading
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, events, sync

api_id = 10787535
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'

def main():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    cursor = mydb.cursor()
    
    while True:
        cursor.execute("SELECT * FROM queries")
        record = cursor.fetchall()
        for i in range(len(record)):
            if record[i][5] == 'block':
                 client = TelegramClient(record[i][1]), api_id, api_hash) 
                 try:
                      client.connect()
                 except Exception as ex:
                      print(ex)
                 full = client(GetFullUserRequest(record[i][2])))
                 if full.user.status != None:
                      print("unblocked")
                 else: 
                      print("blocked")                     
                 client.disconnect()
        break
    
    
#    cursor.execute("SELECT * FROM queries WHERE uniq=%s and name=%s and phone=%s and goal=%s",  (uniq_key, name, phone, goal))
#    record = cursor.fetchone()
#    if record == None:
#        cursor.execute("INSERT INTO queries (uniq, name, phone, goal, time) VALUES (%s, %s, %s, %s, %s)", (uniq_key, name, phone, goal, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mydb.commit()
    cursor.close()
    mydb.close()
    
main()
