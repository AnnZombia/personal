from telethon import TelegramClient, events, sync
import auth

def main():
    auth.main()
    print(auth.client.get_me().username)
    auth.client.send_message('annzombia2', 'hi')				
    auth.client.disconnect()
