from flask import Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
api = Api(app)

@app.route('/auth', methods=['POST'])
def auth_phone():
    global auth_phone
    auth_phone = request.args.get('phone', type=int)

@app.route('/code', methods=['POST'])
def auth_code():
    code = request.args.get('code', type=int)
    return code
	
if __name__ == '__main__':
	app.run(port=1234,host='0.0.0.0')