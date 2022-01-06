import mysql.connector
from mysql.connector import Error

def connectToMySQL(hostString, databaseString, userString, passwordString):
    
    try:
        conn = mysql.connector.connect(host=hostString, database = databaseString, user=userString, password=passwordString) 
        print ("SQL Bağlandı!")
    	
    except Error as e:
        print (e)

    cursor = conn.cursor()

    return conn, cursor

def queryToMySQL(cursor, conn, queryString):

    cursor.execute(queryString)
    conn.commit()