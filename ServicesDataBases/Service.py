import os
import sqlite3

from Model.app_models import University, Usuarios


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
    #
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
    def get_all_universidades(self,):
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
                                                  usuario.password
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


