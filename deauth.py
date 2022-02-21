import os
import auth
import multiprocessing
from multiprocessing import Process, Event
from flask import request, Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
app.debug = False

@app.route('/deauth', methods=['POST'])
def deauth():
    parser = reqparse.RequestParser()
    parser.add_argument("uniq_key")
    params = parser.parse_args()
    uniq_key = params["uniq_key"] 
#    os.remove(uniq_key+".session")
    os.remove("AnnZombia.session")
  
    responce.status_code = 200
    return responce

def api():
    app.run(port=1234,host='0.0.0.0')

def main():
    auth.main()
    multi = multiprocessing.Process(target=api)
    multi.start()

main()
