from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import pyodbc
import configparser

sqlconfig = configparser.ConfigParser()
sqlconfig.read('config.ini')

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
