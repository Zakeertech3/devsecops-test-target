import sqlite3

def get_user_data(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Using raw f-strings for SQL queries instead of parameterized queries
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    return cursor.fetchall()