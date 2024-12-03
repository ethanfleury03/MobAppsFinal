import mysql.connector
from mysql.connector import Error
import bcrypt
import csv
import sys


def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd = 'Ethan88ninja',
            database = 'PetFinder'
        )

    except Error as e:
        return None
    
def add_user(username, password):
    try:
        conn = connect_to_database()
        if conn is None:
            return False
        
        cur = conn.cursor()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert the new user into the database
        query = "INSERT INTO users (UsernameUsers, PasswordUsers) VALUES (%s, %s)"
        cur.execute(query, (username, hashed_password))
        conn.commit()

        print("User added successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def check_login(username, password):
    try:
        connection = connect_to_database()
        if connection is None:
            return False

        cur = connection.cursor()

        query = "SELECT PasswordUsers FROM users WHERE UsernameUsers = %s"
        cur.execute(query, (username,))
        result = cur.fetchone()

        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print('Login Succesful')
                return True
            else:
                print("Invalid password")
                return False
        else:
            print("User not found.")
            return False
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            cur.close()
            connection.close()