import mysql.connector
import multiprocessing
from multiprocessing import Process, Event
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.debug = False
event = multiprocessing.Event()

@app.route('/auth_code', methods=['POST'])
def auth_code():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("phone")
    parser.add_argument("code")
    params = parser.parse_args()
    phone = int(params["phone"])
    code = int(params["code"])
    cursor = mydb.cursor()
    cursor.execute("UPDATE auth SET code=%s WHERE phone = %s", (code, phone))
    mydb.commit()
    cursor.close()
    mydb.close()
    event.clear()
    return ("success")

def api():
    app.run(port=1234,host='0.0.0.0')

def main():
    event.set()
    multi = multiprocessing.Process(target=api)
    multi.start()
    while True:
        if event.is_set() != True:
            multi.terminate()
            multi.join()
            break
