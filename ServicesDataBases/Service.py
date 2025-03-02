import json
import os
import sqlite3


from Model.app_models import University, Usuarios
from utlis.funciones_utlis import generate_salt


class ServiceData:
    def __init__(self):
        self._con = os.path.abspath('DataBases/db')
        self._strcon = ''

    @property
    def con(self):
        return self._con

    @con.setter
    def con(self, con):
        self._con = con

    @property
    def strcon(self):
        return self._strcon

    @strcon.setter
    def strcon(self, strcon):
        self._strcon = strcon

    def conectar_db(self):
        try:
            con = sqlite3.connect(self._con)
            con.row_factory = sqlite3.Row  # Permite obtener los resultados como diccionarios
            self._strcon = con
        except sqlite3.Error as e:
            print(f'Error al conectar: {e}')
            return None

    def create_universidad(self, universidad: University):
        con = self._strcon

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
                            'universidad_id': universidad.universidad_id,
                            'nombre_universidad': universidad.nombre_universidad,
                            'acronimo_universidad': universidad.acronimo_universidad,
                            'foto': universidad.foto
                        }
                        }
            return None

        except sqlite3.Error as e:
            print(f'Error en la consulta: {e}')
            return None

    # Obtener todas las universidades y devolver un objeto JSON clave-valor
    def get_all_universidades(self):
        con = self._strcon
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

    def get_one_universidad(self,id):
        con = self._strcon
        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

        try:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM Universidad where universidad_id = ? ", [id])
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

    def get_all_usuario(self):
        con = self._strcon
        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

        try:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario")
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

    def get_one_usuario(self,id):
        con = self._strcon
        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

        try:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario where username = ? ", [id])
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

    def create_usuario(self, usuario: Usuarios):
        con = self._strcon

        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

        try:
            cursor = con.cursor()
            datos_insertados = cursor.execute("INSERT into usuario values(?,?,?,?)",
                                              (
                                                  usuario.usuario_id.lower(),
                                                  usuario.username.lower(),
                                                  usuario.email.lower(),
                                                  generate_salt(usuario.password)
                                              ))

            if datos_insertados.rowcount > 0:
                con.commit()
                return {'status': 'success',
                        'data': {
                            'usuario_id':  usuario.usuario_id,
                        }
                        }
            return None

        except sqlite3.Error as e:
            print(f'Error en la consulta: {e}')
            return None

    import sqlite3
    import json

    def get_user_subjects(self, user_id):
        con = self._strcon

        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

        query = """
      SELECT 
    u.universidad_id,
    u.acronimo_universidad AS acronym,
    u.nombre_universidad AS name,
    u.foto AS logo,
    json_group_array(
        json_object(
            'subject_name', a.nombre,
            'day', a.dia,
            'start', a.hora_inicio,
            'end', a.hora_fin,
            'room', a.aula
        )
    ) AS subjects
FROM Universidad u
JOIN Asignatura a ON u.universidad_id = a.universidad_id
WHERE a.username = ?
GROUP BY u.universidad_id
ORDER BY 
    CASE 
        WHEN a.dia = 'lunes' THEN 1
        WHEN a.dia = 'martes' THEN 2
        WHEN a.dia = 'miércoles' THEN 3
        WHEN a.dia = 'jueves' THEN 4
        WHEN a.dia = 'viernes' THEN 5
        WHEN a.dia = 'Sabado' THEN 6
        ELSE 7
    END ,
    a.hora_inicio desc;
        """

        cursor = con.cursor()
        cursor.execute(query, [user_id])
        results = cursor.fetchall()

        con.close()  # Cerrar la conexión

        # Convertir resultados a lista de diccionarios
        universidades = []
        for row in results:
            universidades.append({
                "university_id": row[0],
                "acronym": row[1],
                "name": row[2],
                "logo": row[3],
                "subjects": json.loads(row[4]) if row[4] else None  # Convertir JSON string a lista
            })

        return  universidades

