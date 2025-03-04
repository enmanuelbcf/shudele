import bcrypt
from datetime import datetime

import pytz


def generate_salt(password: str):
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt)

def vefify_salt(password: str, salt: bytes):
    psd = password.encode('utf-8')
    if bcrypt.checkpw(psd, salt):
        return True
    else:
        return False

def convert_time(time_str):
    try:
        return datetime.strptime(time_str, "%I:%M %p").time()  # Convierte a formato 24h
    except ValueError:
        print(f"Error en la hora: {time_str}")  # Maneja errores si la hora no es válida
        return datetime.strptime("11:59 PM", "%I:%M %p").time()


def convert_utc_to_dominican(utc_input):
    """
    Convierte un string en formato 'YYYY-MM-DD HH:MM AM/PM' (hora UTC)
    a una cadena en formato 'YYYY-MM-DD HH:MM AM/PM' en la zona horaria de República Dominicana.

    Parámetros:
      - utc_input: string con fecha y hora en formato '2025-03-03 11:58 PM'.

    Retorna:
      - Cadena formateada en 12 horas con la hora de República Dominicana.
    """
    # Se asume que el string sigue el formato "%Y-%m-%d %I:%M %p"
    try:
        utc_dt = datetime.strptime(utc_input, "%Y-%m-%d %I:%M %p")
    except Exception as e:
        raise ValueError("Formato de fecha incorrecto. Use 'YYYY-MM-DD HH:MM AM/PM'") from e

    # Asumimos que el datetime es UTC (naive), lo localizamos a UTC
    utc_dt = pytz.utc.localize(utc_dt)

    dominican_tz = pytz.timezone("America/Santo_Domingo")
    dominican_time = utc_dt.astimezone(dominican_tz)

    # Retorna el resultado en formato 12 horas
    return dominican_time.strftime("%Y-%m-%d %I:%M %p")

print(convert_utc_to_dominican('2025-03-03 11:58 PM'))
