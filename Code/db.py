import sqlite3
from datetime import datetime

def initialize():
    '''Inicializa la base de datos con tabla 'registros' '''
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS registros
                        (estado text, fecha text)''')
    except sqlite3.Error as error:
        raise 
    finally:
        con.close()

                
def save_state(state: str, date:str):
    '''Guarda el estado en la tabla 'registros' de la base de datos'''
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        cur.execute(f"INSERT INTO registros VALUES ('{state}','{date}')")
        con.commit()
    except sqlite3.Error as error:
        print(error)
        raise
    finally:
        con.close()

       
def get_last_state():
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM registros ORDER BY fecha DESC LIMIT 1 ")
        
        row = cur.fetchone()
        if row != None:
            [state, time] = row

            if state == 'con_mascara':
                state = True
            else:
                state= False

            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

            return state, time

    except sqlite3.Error as error:
        raise
    finally:
        con.close()


def get_session_data(start_time: datetime):
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        cur.execute(f"SELECT estado FROM registros WHERE fecha > '{start_time}'")
        
        session_data = []
        data = cur.fetchall()
        data = [x[0] for x in data] 

        for st in data:
            if st == 'con_mascara':
                state = True
            else:
                state = False
            
            session_data.append(state)

        return session_data

    except sqlite3.Error as error:
        raise
    finally:
        con.close()

