import datetime
from telethon.tl.functions.users import GetFullUserRequest
import mysql.connector
import threading
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, events, sync

status = None
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
            full = client(GetFullUserRequest(record[i][1]))
            if record[i][3] == 'block':
                if full.user.status != None:
                    print(full)
                    cursor.execute("INSERT INTO blocked (uniq, name, phone, time) VALUES (%s, %s, %s, %s)", (record[i][0], record[i][1], record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            if record[i][3] == 'status':
                cursor.execute("SELECT * FROM status WHERE uniq=%s and name=%s and phone=%s",  (record[i][0], record[i][1], record[i][2]))
                record = cursor.fetchall()
                last_status = record[len(record)-1][3]
                print(last_status)
                
            if isinstance(full.user.status, UserStatusOffline):
                if last_status == None or last_status == 'Online':
                    cursor.execute("INSERT INTO status (uniq, name, phone, status, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Offline', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                elif last_status == 'Offline':
                    continue
            if isinstance(full.user.status, UserStatusOnline):
                if last_status == None or last_status == 'Offline':
                    cursor.execute("INSERT INTO status (uniq, name, phone, status, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Online', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                elif last_status == 'Online':
                    continue                           
            
            client.disconnect()
        break
    
    
    mydb.commit()
    cursor.close()
    mydb.close()
    
main()
