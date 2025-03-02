import bcrypt
from datetime import datetime


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
    return datetime.strptime(time_str, "%I:%M %p").time()