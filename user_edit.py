import os
import datetime
import auth
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

@app.route('/get_user', methods=['POST'])
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
    if goal != 'delete':
        cursor.execute("INSERT INTO queries (name, phone, prey_name, prey_phone, goal, time) VALUES (%s, %s, %s, %s, %s, %s)", (my_name, my_phone, prey_name, prey_phone, goal, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        cursor.execute("DELETE FROM queries WHERE phone=%s and WHERE prey_phone=%s and prey_name=%s", (my_phone, prey_phone, prey_name))
                    
    mydb.commit()
    cursor.close()
    mydb.close()
    event.clear()
    return "200"

def api():
    app.run(port=1235,host='0.0.0.0')

def main():
    auth.main()
    event.set()
    global my_name
    global my_phone
    my_name = auth.client.get_me().username
    my_phone = auth.client.get_me().phone
    multi = multiprocessing.Process(target=api)
    multi.start()
    while True:
      if event.is_set() != True:
        multi.terminate()
        multi.join()
        break
main()
