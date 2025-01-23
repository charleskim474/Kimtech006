#admini
import sqlite3

class Admin:
    def __init__(self):
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        query="""CREATE TABLE IF NOT EXISTS bonus(date TEXT, id INTEGER, username TEXT, tel TEXT, name TEXT)"""
        cursor.execute(query)
        conn.commit()
        conn.close()
        
    def bonus(self, date, id, uname, tel, name):
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        query="""INSERT INTO bonus(date, id, username,tel, name ) VALUES (?,?,?,?,?)"""
        values=[date, id, uname, tel, name ]
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return 1
        