import sqlite3
from Model.university_model import University


def conectar_db():
    try:
        con = sqlite3.connect('./DataBases/db')
        con.row_factory = sqlite3.Row  # Permite obtener los resultados como diccionarios
        return con
    except sqlite3.Error as e:
        print(f'Error al conectar: {e}')
        return None

def create_universidad(universidad: University ):
    con = conectar_db()
    if con is None:
        return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

    try:
        cursor = con.cursor()
        datos_insertados = cursor.execute("INSERT into Universidad values(?,?,?,?)",
                                          (
            universidad.universidad_id,
            universidad.nombre_universidad,
            universidad.acronimo_universidad,
            universidad.foto
        ))


        if datos_insertados.rowcount > 0:
            con.commit()
            return {'status': 'success',
                    'data': {
                        'universidad_id':universidad.universidad_id,
                        'nombre_universidad':universidad.nombre_universidad,
                        'acronimo_universidad': universidad.acronimo_universidad,
                        'foto': universidad.foto
                        }
                    }
        return  None

    except sqlite3.Error as e:
        print(f'Error en la consulta: {e}')
        return None





# Obtener todas las universidades y devolver un objeto JSON clave-valor
def get_all_universidades():
    con = conectar_db()
    if con is None:
        return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Universidad")
        rows = cursor.fetchall()
        con.close()  # Cerrar conexión

        if rows:
            data = [dict(row) for row in rows]
            return data
        else:
            return None

    except sqlite3.Error as e:
        print(f'Error en la consulta: {e}')
        return None

def get_one_universidad(id):
    con = conectar_db()
    if con is None:
        return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Universidad where universidad_id = ? ",[id] )
        rows = cursor.fetchall()
        con.close()  # Cerrar conexión

        if rows:
            data = [dict(row) for row in rows]  # Convertir cada fila en un diccionario clave-valor
            return data
        else:
            return None

    except sqlite3.Error as e:
        print(f'Error en la consulta: {e}')
        return None

