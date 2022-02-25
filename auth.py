import mysql.connector
import time
import asyncio
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import multiprocessing
from flask import request, Flask
from flask_restful import Api, Resource, reqparse

status = {}
app = Flask(__name__)
app.debug = False
api_id = 10787535
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'

def main():
#    loop = asyncio.new_event_loop()
#    asyncio.set_event_loop(loop)
    multi = multiprocessing.Process(target=api)
    multi.start()
 
# первоначальная проверка ключа на уникальность
@app.route('/auth_init', methods=['POST'])
def auth_init():
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"]) 
  
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app",
        get_warnings = True
        )
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM auth WHERE uniq = %s", (uniq_key,))
    record = cursor.fetchone()
    mydb.commit()
    cursor.close()
    mydb.close()
    if record == None:
        return "200"
    else:
        return "500"

# начало регистрации
@app.route('/auth_phone', methods=['POST'])
def auth_phone():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("phone")
    parser.add_argument("password")
    parser.add_argument("name")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"]) 
    phone = int(params["phone"])
    name = params["name"]
    password = params["password"]
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO auth (name, phone, uniq, password) VALUES (%s, %s, %s, %s)", (name, phone, uniq_key, password))
    mydb.commit()
    cursor.close()
    mydb.close()

    
    global status
    print(phone)
    status = {phone:0}
    print("status = "+str(status.get(phone)))
    multi = multiprocessing.Process(target=login, args=(uniq_key, phone, password))
    multi.start()
    return "200"

# получаем код и выполняем вход
@app.route('/auth_code', methods=['POST'])
def auth_code():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("code")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"])
    code = int(params["code"])
    cursor = mydb.cursor(buffered=True)
    cursor.execute("UPDATE auth SET code=%s WHERE uniq = %s", (code, uniq_key))
    mydb.commit()
    cursor.execute("SELECT phone FROM auth WHERE uniq = %s", (uniq_key,))
    mydb.commit()
    record = cursor.fetchone()
    cursor.close()
    mydb.close()
    phone = '+'+str(record[0])
    
    global status
    print(phone)
    state = {str(record[0]):1}
    status.update(state)
    print(status)
    return "200"
    
                                    
def login(uniq, phone_num, passw):
    uniq_key = uniq
    phone = phone_num
    password = passw
    global status
    
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
                    
    client = TelegramClient(str(uniq_key), api_id, api_hash) 
    client.connect()
    client.send_code_request('+'+str(phone))
    print("i`m here")
    while True:
        if status.get(phone) == 1:
            print("while works")
            break
        time.sleep(60)
        print("bad news")
        print(status.get(phone))
    
    print("while broke")
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT code FROM auth WHERE uniq = %s", (uniq_key,))
    record = cursor.fetchone()
    cursor.close()
    mydb.close()
                                    
    try:
        client.sign_in(phone, str(record[0]))
        return "200"
    except SessionPasswordNeededError:
        client.sign_in(password)
        return "200"
    client.disconnect() 
    del status[phone]
    return "200"
    
def api():
    app.run(port=1234,host='0.0.0.0')
    
main()
