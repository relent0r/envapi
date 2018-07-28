from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import pyodbc
import configparser
from json import dumps
from flask_jsonpify import jsonify
from startup import get_ip
import IdentityManager
import ServerManager

#Get primary IP for web server binding
ip_address = get_ip()

app = Flask(__name__)
api = Api(app)



api.add_resource(IdentityManager.Login, '/login')
api.add_resource(ServerManager.Servers, '/servers') # Route_1
api.add_resource(ServerManager.Servers_Name, '/servers/<client_id>') # Route_3
api.add_resource(IdentityManager.UserQuery, '/users/<username>') # Route_2
api.add_resource(IdentityManager.UserAPI, '/users') # Route_2



if __name__ == '__main__':
     app.run(host=ip_address, port='5002')
     