import datetime
from telethon.tl.functions.users import GetFullUserRequest
import mysql.connector
import threading
from multiprocessing import Process, Event
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.debug = False

@app.route('/del_user', methods=['POST'])
def del_user():
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("name")
    parser.add_argument("phone")
    parser.add_argument("goal")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"])
    phone = params["phone"]
    name = params["name"]
    goal = params["goal"] 
    cursor = mydb.cursor()
    
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )    
    cursor.execute("DELETE FROM queries WHERE uniq=%s and phone=%s and name=%s and goal=%s", (uniq_key, phone, name, goal))       
    mydb.commit()
    cursor.close()
    mydb.close()
    return "200"


@app.route('/add_user', methods=['POST'])
def add_user():
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("name")
    parser.add_argument("phone")
    parser.add_argument("goal")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"])
    phone = params["phone"]
    name = params["name"]
    goal = params["goal"] 

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM queries WHERE uniq=%s and name=%s and phone=%s and goal=%s",  (uniq_key, name, phone, goal))
    record = cursor.fetchone()
    if record == None:
        cursor.execute("INSERT INTO queries (uniq, name, phone, goal, time) VALUES (%s, %s, %s, %s, %s)", (uniq_key, name, phone, goal, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mydb.commit()
    cursor.close()
    mydb.close()
    return "200"

def api():
    app.run(port=1235,host='0.0.0.0')

def main():
    thread1 = threading.Thread(target=api)
    thread1.start()
    
main()
