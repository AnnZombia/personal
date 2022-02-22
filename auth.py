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

app = Flask(__name__)
app.debug = False
api_id = 10787535
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'

def main():
    global client
    app.run(port=1234,host='0.0.0.0')
 
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
    client = TelegramClient(str(uniq_key), api_id, api_hash) 
    client.connect()
    client.send_code_request('+'+(params["phone"]))
    time.sleep(60)
    client.disconnect() 
    return "200"

# получаем код и выполняем вход
@app.route('/auth_code', methods=['POST'])
def auth_code():
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
    cursor = mydb.cursor()
    cursor.execute("UPDATE auth SET code=%s WHERE uniq = %s", (code, uniq_key))
    mydb.commit()
    cursor.execute("SELECT phone, password FROM auth WHERE uniq_key = %s", (uniq_key,))
    record = cursor.fetchone()
    mydb.commit()
    cursor.close()
    mydb.close()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(str(uniq_key), api_id, api_hash, loop=loop) 
    client.connect()
    try:
      client.sign_in(phone, code)
      return "200"
    except SessionPasswordNeededError:
      client.sign_in(password)
      return "200"
    client.disconnect() 
        
main()
