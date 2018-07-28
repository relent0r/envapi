from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
import SQLManager
import jwt
import datetime

class UserAPI(Resource):   # honestly I should probably put this into another class..tomorrow. 
    def post(self):
        try:  
            from bcrypt import hashpw, gensalt
            import uuid
            # request into json variable
            post_content = request.get_json()
            # start extracting properties
            username = post_content['username']
            password = post_content['password']
            # hash the password
            passhash = hashpw(password.encode('utf-8'), gensalt(14))
            firstname = post_content['firstname']
            lastname = post_content['lastname']
            emailaddress = post_content['email']
            uuid = uuid.uuid4()
            # get datetime for created column
            i = datetime.datetime.now()
            datecreated = i.isoformat()
            #check if null values, this doesn't really work with json input tbh
            if username is None or password is None or firstname is None or lastname is None or emailaddress is None:
                abort(400) # invalid parameters
                return 
            conn = SQLManager.MSSQLDatabase()   
            conn.query("""INSERT INTO dbo.users (username, firstname, lastname, emailaddress, password, created, uuid) VALUES (?, ?, ?, ?, ?, ?, ?)""", [username, firstname, lastname, emailaddress, passhash, datecreated, uuid])
            conn.commit() # don't forget to commit your change
        except Exception as e:
            print('error :' + str(e))
            return {'error': str(e)}
        return ('User ' + username + ' Added')

class UserQuery(Resource):
    def get(self, username):
        conn = SQLManager.MSSQLDatabase()
        cursor = conn.query("""SELECT username, firstname, lastname, emailaddress FROM dbo.users WHERE username = ?""", [username])
        return {'userdetails': [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]}    

class Login(Resource):
    def post(self):
        post_content = request.get_json()
        print(post_content)
        username = post_content['username']
        try:
            conn = SQLManager.MSSQLDatabase()
            cursor = conn.query("""SELECT username FROM dbo.users WHERE username = ?""", [username])
            data = cursor.fetchall()
            if data:
                print ('user exist', data)
                return {'User Exist': [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]}
            else:
                print ('user not exist', data)
                return {'User not Exist': [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]}
        except Exception as e:
            return {'error': str(e)}
        

def encode_auth_token(self, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e
  
def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'