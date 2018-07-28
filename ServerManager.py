from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import pyodbc
import configparser
import SQLManager

sqlconfig = configparser.ConfigParser()
sqlconfig.read('config.ini')

class Servers(Resource):
    def get(self):
        conn = SQLManager.MSSQLDatabase()
        params = None
        cursor = conn.query("""SELECT name, cpu, memory FROM dbo.servers""")
        return {'servers': [i[0] for i in cursor.fetchall()]}

class Servers_Name(Resource):
    def get(self, client_id):
        conn = SQLManager.MSSQLDatabase()
        cursor = conn.query("""SELECT name, cpu, memory FROM dbo.servers WHERE clientid = ?""", [client_id])
        return {'servers': [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]}
