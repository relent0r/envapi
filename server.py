from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import pyodbc
import configparser
from json import dumps
from flask_jsonpify import jsonify
from startup import get_ip

#Get primary IP for web server binding
ip_address = get_ip()
sqlconfig = configparser.ConfigParser()
sqlconfig.read('config.ini')
app = Flask(__name__)
api = Api(app)

class Servers(Resource):
    def get(self):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['database'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()
        query = cursor.execute("""SELECT name, cpu, memory FROM dbo.servers""")
        return {'servers': [i[0] for i in query.fetchall()]}

class Servers_Name(Resource):
    def get(self, client_id):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['database'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()
        query = cursor.execute("""SELECT name, cpu, memory FROM dbo.servers WHERE clientid = ?""", client_id)
        return {'servers': [dict(zip([column[0] for column in cursor.description], row)) for row in query.fetchall()]}

class UserQuery(Resource):
    def get(self, username):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['identitydb'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()
        query = cursor.execute("""SELECT username, firstname, lastname, emailaddress FROM dbo.users WHERE username = ?""", username)
        return {'userdetails': [dict(zip([column[0] for column in cursor.description], row)) for row in query.fetchall()]}    

class UserAPI(Resource):    
    def post(self):
        import datetime
        jsoncontent = request.get_json()
        username = jsoncontent['username']
        password = jsoncontent['password']
        firstname = jsoncontent['firstname']
        lastname = jsoncontent['lastname']
        emailaddress = jsoncontent['email']
        i = datetime.datetime.now()
        datecreated = i.isoformat()
        if username is None or password is None or firstname is None or lastname is None or emailaddress is None:
            abort(400) # invalid parameters
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['identitydb'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()   
        cursor.execute("""INSERT INTO dbo.users (username, firstname, lastname, emailaddress, password, created) VALUES (?, ?, ?, ?, ?, ?)""", username, firstname, lastname, emailaddress, password, datecreated)
        cursor.commit()
        return ('User ' + username + ' Added')

api.add_resource(Servers, '/servers') # Route_1
api.add_resource(Servers_Name, '/servers/<client_id>') # Route_3
api.add_resource(UserQuery, '/users/<username>') # Route_2
api.add_resource(UserAPI, '/users') # Route_2


if __name__ == '__main__':
     app.run(host=ip_address, port='5002')
     