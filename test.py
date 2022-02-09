from flaskext.mysql import MySQL
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)

@app.route('/auth_phone', methods=['POST'])
def auth_phone():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    phone = request.args.get('phone')
    cursor = mydb.cursor()
    cursor.execute(''' INSERT INTO auth (phone) VALUES (%s) ''', phone)
    mydb.commit()
    cursor.close()
    mydb.close()

@app.route('/auth_code', methods=['POST'])
def auth_code():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Aksenov/1",
        database = "app"
        )
    code = request.args.get('code')
    phone = request.args.get('phone')
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO auth (code) WHERE phone = %s VALUES (%s)''', (phone, code))
    mysql.connection.commit()
    cursor.close()
    mydb.close()

if __name__ == '__main__':
	app.run(port=1234,host='0.0.0.0')
