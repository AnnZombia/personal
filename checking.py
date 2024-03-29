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
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    cursor = mydb.cursor(buffered=True) 
    while True:   
# вытаскиваем список активных проверок
        cursor.execute("SELECT * FROM queries")
        record = cursor.fetchall()
        print(record)
        mydb.commit()

# для каждой проверки отдельно подключаемся и выполняем требуемый запрос
        for i in range(len(record)):
            print(record[i][0])
            client = TelegramClient(str(record[i][0]), api_id, api_hash) 
            try:
                client.connect()
            except Exception as ex:
                print(ex)
            full = client(GetFullUserRequest(str(record[i][1])))

# проверяем запрос на актуальность блокировки
            if record[i][3] == 'block':
                if full.user.status != None:
 
# если пользователь оказался разблокирован - записываем время и удаляем запрос из БД
                    cursor.execute("INSERT INTO blocked (uniq, name, phone, time) VALUES (%s, %s, %s, %s)", (record[i][0], record[i][1], record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    mydb.commit()
        
# условия на случай, если имя или номер не были внесены
                    if record[i][2] == None:
                        cursor.execute("DELETE FROM queries WHERE uniq=%s and name=%s and goal=%s",  (record[i][0], record[i][1], 'block'))
                    elif record[i][1] == None:
                        cursor.execute("DELETE FROM queries WHERE uniq=%s and phone=%s and goal=%s",  (record[i][0], record[i][2], 'block'))
                    else:
                        cursor.execute("DELETE FROM queries WHERE uniq=%s and name=%s and phone=%s and goal=%s",  (record[i][0], record[i][1], record[i][2], 'block'))
                    mydb.commit()
                    
# проверяем статус запрошенного пользователя
            if record[i][3] == 'status':
                cursor.execute("SELECT * FROM status WHERE uniq=%s and name=%s and phone=%s",  (record[i][0], record[i][1], record[i][2]))
                record1 = cursor.fetchall()
                mydb.commit()
                
# фиксируем последний статус, если это первый запрос по пользователю - ставим статус Offline
                if len(record1) != 0:
                    last_status = record1[len(record1)-1][3]
                else:
                    last_status = 'Offline'
                    
# если текущий статус Offline, и это отличается от последнего - пишем в БД и обновляем значение последнего статуса
                if isinstance(full.user.status, UserStatusOffline):
                    if last_status == None or last_status == 'Online':
                        cursor.execute("INSERT INTO status (uniq, name, status, phone, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Offline', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        mydb.commit()
                    elif last_status == 'Offline':
                        continue
                        
# если текущий статус Online, и это отличается от последнего - пишем в БД и мобновляем значение последнего статуса                                                
                if isinstance(full.user.status, UserStatusOnline):
                    if last_status == None or last_status == 'Offline':
                        cursor.execute("INSERT INTO status (uniq, name, status, phone, time) VALUES (%s, %s, %s, %s, %s)", (record[i][0], record[i][1], 'Online', record[i][2], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        mydb.commit()
                    elif last_status == 'Online':
                        continue                           
                        
            client.disconnect()
        time.sleep(5)
    mydb.close()
   
    
main()
