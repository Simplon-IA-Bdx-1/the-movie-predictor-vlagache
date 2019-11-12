import os
import mysql.connector

class DbFactory:

    def __init__(self):
        password = os.environ['MYSQL_PASSWORD']
        db = mysql.connector.connect(user='predictor', password=password,
                                host='database', #127.0.0.1
                                database='predictor')
        self.cnx = db # cnx

    def db_connect(self):
        return self.cnx
    
    def db_disconnect(self):
        self.cnx.close()
    
    def create_cursor(self):
        return self.cnx.cursor(dictionary=True)
    
    def close_cursor(self):
        cursor = self.create_cursor()
        cursor.close()



