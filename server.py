from flask import Flask, request
from flask_restful import Resource, Api
import pyodbc
import configparser
from json import dumps
from flask_jsonpify import jsonify

sqlconfig = configparser.ConfigParser()
sqlconfig.read('config.ini')
app = Flask(__name__)
api = Api(app)

class Servers(Resource):
    def get(self):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['database'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()
        query = cursor.execute("""SELECT name, cpu, memory FROM dbo.servers""")
        return {'servers': [i[0] for i in query.fetchall()]} # Fetches first column that is Employee ID

class Servers_Name(Resource):
    def get(self, client_id):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['database'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()
        query = cursor.execute("""SELECT name, cpu, memory FROM dbo.servers WHERE clientid = ?""", client_id)
        return {'servers': [dict(zip([column[0] for column in cursor.description], row)) for row in query.fetchall()]}
        

api.add_resource(Servers, '/servers') # Route_1
api.add_resource(Servers_Name, '/servers/<client_id>') # Route_3


if __name__ == '__main__':
     app.run(host='10.1.1.101', port='5002')
     