import json
import psycopg2
import psycopg2.extras
from datetime import datetime
import pytz
from Model.app_models import University, Usuarios, Asignatura, UsuariosCreate
from utlis.funciones_utlis import generate_salt


class ServiceData:
    def __init__(self):
        self._host = "shuttle.proxy.rlwy.net"
        self._port = 14117
        self._dbname = "railway"
        self._user = "postgres"
        self._password = "EuCAmwNXtVftyvrLzbpsoTSNPGvzloRk"
        self._strcon = None

    def conectar_db(self):
        try:
            con = psycopg2.connect(
                host=self._host,
                port=self._port,
                dbname=self._dbname,
                user=self._user,
                password=self._password
            )
            con.autocommit = False
            self._strcon = con
            return con
        except psycopg2.Error as e:
            print(f"Error al conectar: {e}")
            return None

    def create_universidad(self, universidad: University):
        con = self._strcon
        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

        try:
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO Universidad (universidad_id, nombre_universidad, acronimo_universidad, foto)
                VALUES (%s, %s, %s, %s)
            """, (
                universidad.universidad_id,
                universidad.nombre_universidad,
                universidad.acronimo_universidad,
                universidad.foto
            ))
            con.commit()
            return {'status': 'success', 'data': universidad.__dict__}
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def get_all_universidades(self):
        con = self._strcon
        if con is None:
            return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM Universidad")
            rows = cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def get_one_universidad(self, id):
        con = self._strcon
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM Universidad WHERE universidad_id = %s", [id])
            rows = cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def get_all_usuario(self):
        con = self._strcon
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM usuario")
            return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def get_one_usuario(self, id):
        con = self._strcon
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM usuario WHERE username = %s", [id])
            return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def create_usuario(self, usuario: UsuariosCreate):
        con = self._strcon
        try:
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO usuario (username, email, password)
                VALUES (%s, %s, %s)
            """, (
                usuario.username.upper(),
                usuario.email.lower(),
                generate_salt(usuario.password)
            ))
            con.commit()
            return {'status': 'success'}
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def registrar_asignatura(self, asignatura: Asignatura):
        con = self._strcon
        try:
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO asignatura (nombre, dia, hora_inicio, hora_fin, aula, universidad_id, username)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING asignatura_id
            """, (
                asignatura.nombre,
                asignatura.dia,
                asignatura.hora_inicio,
                asignatura.hora_fin,
                asignatura.aula,
                asignatura.universidad_id,
                asignatura.username
            ))
            asignatura_id = cursor.fetchone()[0]
            con.commit()
            return {
                "asignatura": asignatura_id,
                "nombre": asignatura.nombre,
                "dia": asignatura.dia,
                "hora_inicio": asignatura.hora_inicio,
                "hora_fin": asignatura.hora_fin,
                "aula": asignatura.aula,
                "universidad_id": asignatura.universidad_id,
                "username": asignatura.username
            }
        except psycopg2.Error as e:
            print("Error en la base de datos:", e)
            return None
        finally:
            cursor.close()

    def get_user_subjects(self, user_id):
        con = self._strcon
        try:
            cursor = con.cursor()
            cursor.execute("""
                SELECT 
                    u.universidad_id,
                    u.acronimo_universidad,
                    u.nombre_universidad,
                    u.foto,
                    json_agg(
                        json_build_object(
                            'subject', a.nombre,
                            'day', a.dia,
                            'start', a.hora_inicio,
                            'end', a.hora_fin,
                            'room', a.aula
                        )
                    ) AS subjects
                FROM Universidad u
                JOIN Asignatura a ON u.universidad_id = a.universidad_id
                WHERE a.username = %s
                GROUP BY u.universidad_id
            """, [user_id])

            universidades = []
            for row in cursor.fetchall():
                universidades.append({
                    "university_id": row[0],
                    "acronym": row[1],
                    "name": row[2],
                    "logo": row[3],
                    "subjects": row[4]
                })
            return universidades
        except psycopg2.Error as e:
            print("Error en la consulta:", e)
            return None
        finally:
            cursor.close()

    def obtener_asignaturas_por_dia(self, dia):
        con = self._strcon
        dia_actual_utc = datetime.now(pytz.utc)
        try:
            cursor = con.cursor()
            cursor.execute("""
                SELECT A.hora_inicio, A.hora_fin, U.acronimo_universidad, A.nombre
                FROM Asignatura A
                JOIN Universidad U ON A.universidad_id = U.universidad_id
                WHERE A.username = 'ediaz' AND A.dia = %s
                ORDER BY A.hora_inicio
            """, [dia])
            asignaturas = cursor.fetchall()

            data = [
                {
                    'hora': datetime.combine(dia_actual_utc.date(), datetime.strptime(hora, "%H:%M").time()).replace(tzinfo=pytz.utc),
                    'hora_fin': datetime.combine(dia_actual_utc.date(), datetime.strptime(hora_fin, "%H:%M").time()).replace(tzinfo=pytz.utc),
                    'nombre_universidad': nombre_universidad,
                    'asignatura': asignatura
                }
                for hora, hora_fin, nombre_universidad, asignatura in asignaturas
            ]
            return data
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")
            return None
        finally:
            cursor.close()

    def insert_historico_servicio(self, nombre_servicio, data):
        con = self._strcon
        try:
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO historico_servicios (nombre_servicio, data)
                VALUES (%s, %s)
            """, [nombre_servicio, data])
            con.commit()
            return True
        except psycopg2.Error as e:
            print("Error al insertar datos:", e)
            return None
        finally:
            cursor.close()

    def get_historico(self):
        con = self._strcon
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM historico_servicios ORDER BY fecha DESC")
            return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()

    def obtener_parametro_por_id(self, parametro):
        con = self._strcon
        try:
            cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM Parametros WHERE parametro_id = %s", [parametro])
            rows = cursor.fetchall()
            return rows[0] if rows else None
        except psycopg2.Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            cursor.close()
