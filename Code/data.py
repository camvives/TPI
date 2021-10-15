import sqlite3



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
    try:
        con =  sqlite3.connect('facemask.db')
        cur = con.cursor()
        cur.execute(f"INSERT INTO registros VALUES ('{state}','{date}')")
        con.commit()
    except sqlite3.Error as error:
        raise
    finally:
        con.close()

       

