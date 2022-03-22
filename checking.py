import datetime
import time
from telethon.tl.functions.users import GetFullUserRequest
import mysql.connector
import threading
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, events, sync
from telethon.tl.types import UserStatusOnline, UserStatusOffline

status = None
api_id = 10787535
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'

def main():
    
    while True:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Aksenov/1",
            database = "app"
            )
        cursor = mydb.cursor()
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
                    print("unblocked!")
                    cursor.execute("INSERT INTO blocked (uniq, name, phone, time) VALUES (%s, %s, %s, %s)", (record[i][0], record[i][1], record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    mydb.commit()
                    print("done")
                    print(record[i][0], record[i][1], record[i][2])
                    if record[i][2] != 'None':
                        cursor.execute("DELETE FROM queries WHERE uniq=%s and name=%s and phone=%s and goal=%s",  (record[i][0], record[i][1], record[i][2], 'block'))
                    else:
                        cursor.execute("DELETE FROM queries WHERE uniq=%s and name=%s and phone=%s and goal=%s",  (record[i][0], record[i][1], '', 'block'))
                    mydb.commit()
            if record[i][3] == 'status':
                cursor.execute("SELECT * FROM status WHERE uniq=%s and name=%s and phone=%s",  (record[i][0], record[i][1], record[i][2]))
                record1 = cursor.fetchall()
                if len(record1) != 0:
                    last_status = record1[len(record1)-1][3]
                    print(last_status)
                else:
                    cursor.execute("INSERT INTO status (uniq, name, status, phone, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Offline', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    mydb.commit()
                if isinstance(full.user.status, UserStatusOffline):
                    if last_status == None or last_status == 'Online':
                        cursor.execute("INSERT INTO status (uniq, name, status, phone, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Offline', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        mydb.commit()
                    elif last_status == 'Offline':
                        continue
                if isinstance(full.user.status, UserStatusOnline):
                    if last_status == None or last_status == 'Offline':
                        cursor.execute("INSERT INTO status (uniq, name, status, phone, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Online', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        mydb.commit()
                    elif last_status == 'Online':
                        continue                           
            client.disconnect()

        cursor.close()
        mydb.close()
        time.sleep(5)
   
    
main()
