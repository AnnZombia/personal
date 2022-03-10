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
            client = TelegramClient(str(record[i][0]), api_id, api_hash) 
            try:
                 client.connect()
            except Exception as ex:
                 print(ex)
            if record[i][3] == 'block':
                 full = client(GetFullUserRequest(record[i][1]))
                 if full.user.status != None:
                      cursor.execute("INSERT INTO blocked (uniq, name, phone, date) VALUES (%s, %s, %s, %s)", (record[i][0], record[i][1], record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                      print(record[i][1]+"unblocke")
            client.disconnect()
        break
    
    
    mydb.commit()
    cursor.close()
    mydb.close()
    
main()
