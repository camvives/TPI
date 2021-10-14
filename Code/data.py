import sqlite3

con =  sqlite3.connect('facemask.db')
cur = con.cursor()

def initialize():
    cur.execute('''CREATE TABLE IF NOT EXISTS registros
                    (estado text, fecha text)''')

def save_state(state: str, date:str):
    cur.execute(f"INSERT INTO registros VALUES ('{state}','{date}')")
    con.commit()

