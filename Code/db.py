import sqlite3
from datetime import datetime, timedelta
import dateutil.relativedelta

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
    '''Obtiene el estado y la fecha del último registro de la tabla 'registros' de la base de datos'''
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

def get_session_data(start_date: datetime):
    '''Obtiene los estados desde que se inició la sesión a ahora'''
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        cur.execute(f"SELECT estado FROM registros WHERE fecha > '{start_date}'")
        
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

def get_month_data():
    '''Obtiene los registros de los ultimos 30 dias'''
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        today = datetime.now().replace(hour=0)
        last_month = datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        cur.execute(f'''SELECT * FROM registros WHERE fecha > '{last_month}' AND fecha < '{today}'  
                        ORDER BY date(fecha) DESC''')

        data_month = cur.fetchall()
        
        return data_month

    except sqlite3.Error as error:
        raise
    finally:
        con.close()

def get_week_data():
    '''Obtiene los registros desde el lunes hasta el dia en curso'''
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        today = datetime.now().replace(hour=0)
        last_monday = today - timedelta(days = today.weekday())
        cur.execute(f"SELECT * FROM registros WHERE fecha > '{last_monday}'")

        data_week = cur.fetchall()
        
        return data_week

    except sqlite3.Error as error:
        raise
    finally:
        con.close()
