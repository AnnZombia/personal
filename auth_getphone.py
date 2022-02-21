import mysql.connector
from multiprocessing import Process
from flask import request, Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.debug = False

@app.route('/auth_phone', methods=['POST'])
def auth_phone():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    parser.add_argument("phone")
    parser.add_argument("name")
    params = parser.parse_args()
    uniq_key = int(params["uniq_key"]) 
    phone = int(params["phone"])
    name = params["name"]
    cursor = mydb.cursor()
    
    # не забыть сделать проверку ключа на уникальность
    
    if name is None:
        cursor.execute("INSERT INTO auth (phone, uniq) VALUES (%s, %s)", (phone, uniq_key))
    elif phone is None:
        cursor.execute("INSERT INTO auth (name, uniq) VALUES (%s, %s)", (name, uniq_key))
    elif name != None and phone != None:
        cursor.execute("INSERT INTO auth (name, phone, uniq) VALUES (%s, %s, %s)", (name, phone, uniq_key))
        
    mydb.commit()
    cursor.close()
    mydb.close()
    return "200"

@app.route('/auth_code', methods=['POST'])
def auth_code():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    parser = reqparse.RequestParser()
    parser.add_argument("name")
    parser.add_argument("phone")
    parser.add_argument("code")
    params = parser.parse_args()
    phone = int(params["phone"])
    code = int(params["code"])
    name = params["name"]
    cursor = mydb.cursor()
    
    if name is None:
        cursor.execute("UPDATE auth SET code=%s WHERE uniq = %s" and phone=%s", (code, uniq_key, phone))
    elif phone is None:
        cursor.execute("UPDATE auth SET code=%s WHERE uniq = %s" and name=%s", (code, uniq_key, name))
    elif name != None and phone != None:
        cursor.execute("UPDATE auth SET code=%s WHERE uniq = %s" and phone=%s and name=%s", (code, uniq_key, phone, name))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return "200"


def api():
    app.run(port=1234,host='0.0.0.0')

def main():
    multi = multiprocessing.Process(target=api)
    multi.start()
