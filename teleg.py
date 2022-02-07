from telethon import TelegramClient, events, sync

name = 'AnnZombia2'
api_id = 10787535 
api_hash = 'f4c93d55681e17b14d516e8f5571e4cd'
client = TelegramClient(name, api_id, api_hash)
client.start()
client.send_message('annzombia', 'hi')				
client.disconnect()