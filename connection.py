import mysql.connector

def connection(user="root", password="", host="localhost", database="practice_flask_web_crud_01"):
    connect = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database,
    )

    return connect