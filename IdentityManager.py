from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import pyodbc
import configparser

sqlconfig = configparser.ConfigParser()
sqlconfig.read('config.ini')

class UserAPI(Resource):   # honestly I should probably put this into another class..tomorrow. 
    def post(self):
        try:
            import datetime
            from bcrypt import hashpw, gensalt
            # request into json variable
            jsoncontent = request.get_json()
            # start extracting properties
            username = jsoncontent['username']
            password = jsoncontent['password']
            # hash the password
            passhash = hashpw(password.encode('utf-8'), gensalt(14))
            firstname = jsoncontent['firstname']
            lastname = jsoncontent['lastname']
            emailaddress = jsoncontent['email']
            # get datetime for created column
            i = datetime.datetime.now()
            datecreated = i.isoformat()
            #check if null values, this doesn't really work with json input tbh
            if username is None or password is None or firstname is None or lastname is None or emailaddress is None:
                abort(400) # invalid parameters
                return 
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['identitydb'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
            cursor = cnxn.cursor()   
            cursor.execute("""INSERT INTO dbo.users (username, firstname, lastname, emailaddress, password, created) VALUES (?, ?, ?, ?, ?, ?)""", username, firstname, lastname, emailaddress, passhash, datecreated)
            cursor.commit() # don't forget to commit your change
        except Exception as e:
            return {'error': str(e)}
        return ('User ' + username + ' Added')

class UserQuery(Resource):
    def get(self, username):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['identitydb'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        cursor = cnxn.cursor()
        query = cursor.execute("""SELECT username, firstname, lastname, emailaddress FROM dbo.users WHERE username = ?""", username)
        return {'userdetails': [dict(zip([column[0] for column in cursor.description], row)) for row in query.fetchall()]}    


 #       def encode_auth_token(self, user_id):
 #           import jwt
 #           """
  #          Generates the Auth Token
 #           :return: string
  #          """
  #          try:
  #              payload = {
  #                  'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
  #                  'iat': datetime.datetime.utcnow(),
  #                  'sub': user_id
  #              }
  #              return jwt.encode(
  #                  payload,
  #                  app.config.get('SECRET_KEY'),
  #                  algorithm='HS256'
  #              )
  #          except Exception as e:
  #              return e