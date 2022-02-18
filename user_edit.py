import os
import datetime
import auth as auth
from telethon.tl.functions.users import GetFullUserRequest
import subprocess
import mysql.connector
import multiprocessing
from multiprocessing import Process, Event
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.debug = False
event = multiprocessing.Event()

@app.post('/get_user')
def get_user():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    
    parser = reqparse.RequestParser()
    parser.add_argument("name")
    parser.add_argument("phone")
    parser.add_argument("goal")
    params = parser.parse_args()
    prey_phone = int(params["phone"])
    prey_name = params["name"]
    goal = params["goal"] 
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO queries (name, phone, prey_name, prey_phone, goal, time) VALUES (%s, %s, %s, %s, %s, %s)", (client.get_me().username, client.get_me().phone, prey_name, prey_phone, goal, datetime.datetime.now().timestamp()))
    mydb.commit()
    cursor.close()
    mydb.close()
    event.clear()
    return 200

def api():
    app.run(port=1235,host='0.0.0.0')

def main():
    event.set()
    multi = multiprocessing.Process(target=api)
    multi.start()
    while True:
      if event.is_set() != True:
        multi.terminate()
        multi.join()
        break
