import sqlite3

def conectar_db():
    try:
        con = sqlite3.connect('../DataBases/dbshedule')
        return con

    except sqlite3.Error as e:
        print(f'{e.sqlite_errorname}-{e.sqlite_errorcode}')

def get_all():
    con = conectar_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Universidad")
    data = cursor.fetchall()
    con.close()
    return data


