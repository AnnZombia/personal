from mysql.connector import connect, Error
from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime
now= datetime.now()
app = Flask(__name__)
api = Api(app)

class telegram(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("phone")
		parser.add_argument("prey")
		parser.add_argument("time")
		params = parser.parse_args()
		date = datetime.strptime(params["time"], '%Y-%m-%d %H:%M:%S')
		phone_num = int(params["phone"])
		try:
			with connect(
				host='localhost',
				user='root',
				password='Aksenov/1',
				db='app'
			) as connection:
				print(connection)
				insert_query = """
				INSERT INTO queries
				(name, phone, prey, time)
				VALUES (%s, %s, %s, %s)
				"""
				parameters = [params["name"], phone_num, params["prey"], date]
				with connection.cursor() as cursor:
					cursor.execute(insert_query, parameters)
					connection.commit()
		except Error as e:
			print(e)
#		responce.status_code = 200
#		return responce

api.add_resource(telegram, "/telegram", "/telegram/")
if __name__ == '__main__':
	app.run(port=1234,host='0.0.0.0')
