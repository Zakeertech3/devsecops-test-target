import sqlite3

def authenticate_user(username, password):
    db_connection = sqlite3.connect('users.db')
    cursor = db_connection.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return True
    return False