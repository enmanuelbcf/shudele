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
    try:
        utc_dt = utc_input.replace(tzinfo=pytz.utc)
    except Exception as e:
        raise ValueError("Formato de fecha incorrecto.") from e

    dominican_tz = pytz.timezone("America/Santo_Domingo")
    dominican_time = utc_dt.astimezone(dominican_tz)

    hora_dom = dominican_time.strftime("%Y-%m-%d %I:%M %p")
    return hora_dom

