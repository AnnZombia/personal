import multiprocessing
import mysql.connector
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
import time
ann = None
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
    parser.add_argument("phone")
    params = parser.parse_args()
    phone = int(params["phone"])
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO auth (phone) VALUES (%s)", (phone, ))
    mydb.commit()
    cursor.close()
    mydb.close()
    return str(phone)

@app.route('/auth_code', methods=['POST'])
def auth_code():
    global ann
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
    ann = 1
    code = int(params["code"])
    cursor = mydb.cursor()
    cursor.execute("UPDATE auth SET code=%s WHERE phone = %s", (code, phone))
    mydb.commit()
    cursor.close()
    mydb.close()
    return str(code)

def api():
    app.run(port=1234,host='0.0.0.0')

multi = multiprocessing.Process(target=api)
multi.start()
#time.sleep(4)
while True:    
    if ann == 1:
        print(ann)
        break
multi.terminate()
print(ann)

#if __name__ == "__main__":
#     main()
