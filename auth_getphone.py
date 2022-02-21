import mysql.connector
import os
import multiprocessing
from multiprocessing import Process, Event
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.debug = False
#event = multiprocessing.Event()

@app.route('/auth_phone', methods=['POST'])
def auth_phone():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("phone")
    params = parser.parse_args()
    phone = int(params["phone"])
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO auth (phone, uniq) VALUES (%s, %s)", (phone, uniq_key))
    mydb.commit()
    cursor.close()
    mydb.close()
#    event.clear()
    responce.status_code = 200
    return responce


@app.route('/deauth', methods=['POST'])
def deauth():
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    params = parser.parse_args()
    uniq_key = params["uniq_key"] 
#    os.remove(uniq_key+".session")
    os.remove("./AnnZombia.session")
    print(os.getcwd())
    responce.status_code = 200
    return responce

def api():
    app.run(port=1234,host='0.0.0.0')

def main(key):
    global uniq_key 
    uniq_key = key
#    event.set()
    multi = multiprocessing.Process(target=api)
    multi.start()
#    while True:
#        if event.is_set() != True:
#            multi.terminate()
#            multi.join()
#            break
