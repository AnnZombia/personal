import datetime
from telethon.tl.functions.users import GetFullUserRequest
import mysql.connector
import threading
from multiprocessing import Process, Event
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.debug = False

@app.route('/get_user', methods=['POST'])
def get_user():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("name")
    parser.add_argument("phone")
    parser.add_argument("goal")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"])
    prey_phone = params["phone"]
    prey_name = params["name"]
    goal = params["goal"] 
    cursor = mydb.cursor()
    
    # adding/deleting prey
    if goal != 'delete':
        cursor.execute("INSERT INTO queries (uniq, prey_name, prey_phone, goal, time) VALUES (%s, %s, %s, %s, %s)", (uniq_key, prey_name, prey_phone, goal, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        cursor.execute("DELETE FROM queries WHERE uniq=%s and prey_phone=%s and prey_name=%s", (uniq_key, prey_phone, prey_name))
                    
    mydb.commit()
    cursor.close()
    mydb.close()
    event.clear()
    return "200"

def api():
    app.run(port=1235,host='0.0.0.0')

def main():
    thread1 = threading.Thread(target=api)
    thread1.start()
    
main()
