import time
import asyncio
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
import threading
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
from telethon import TelegramClient, events, sync

app = Flask(__name__)
app.debug = False
api_id = 10787535
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'

def main():
    thread1 = threading.Thread(target=api)
    thread1.start()
    
    
@app.route('/send_message', methods=['POST'])
def send_message():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    

    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("message")
    parser.add_argument("user")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"])
    message = params["message"]
    user = params["user"]

    
    client = TelegramClient(str(uniq_key), api_id, api_hash) 
    try:
        client.connect()
    except Exception as ex:
        print(ex)
    try:
        client.send_message(user, message)
    except Exception as ex:
        print(ex)
    client.disconnect()

        
def main():
    thread1 = threading.Thread(target=api)
    thread1.start()

def api():
    app.run(port=1234,host='0.0.0.0')
    
main()
