from telethon import TelegramClient, events, sync
import auth

def main():
    auth.main()
    auth.client.send_message('annzombia2', 'hi')				
    auth.client.disconnect()
