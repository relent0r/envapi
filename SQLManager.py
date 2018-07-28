import pyodbc
import configparser

class MSSQLDatabase(object):
    connection = None
    cursor = None 

    def __init__(self):
        sqlconfig = configparser.ConfigParser()
        sqlconfig.read('config.ini')
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (sqlconfig['SQLConfig']['server'], sqlconfig['SQLConfig']['identitydb'], sqlconfig['SQLConfig']['username'], sqlconfig['SQLConfig']['password']))
        self.cursor = self.connection.cursor()

    def query(self, query, params):
        return self.cursor.execute(query, params)

    def commit(self):
        return self.connection.commit()

    def __del__(self):
        self.connection.close()