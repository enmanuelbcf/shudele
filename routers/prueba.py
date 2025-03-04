import threading
import pytz
import requests
import json
from datetime import datetime, timedelta

from ServicesDataBases.Service import ServiceData
from utlis.funciones_utlis import convert_utc_to_dominican

ONESIGNAL_APP_ID = "ebb2b31d-1769-4f6e-8572-7b238fb961a6"
ONESIGNAL_API_KEY = "os_v2_app_5ozlghixnfhw5blspmry7olbuzq3n3rrcsiuznmeh6g77fwsc3x67xsj7lqtku7znyla5ykxfu5tl7m2kji6trihgyhsnqytxnmfoea"


def schedule_notifications(notifications, dia_actual):
    if len(notifications)  < 1:
        print(f'dia - {dia_actual} - no hay notificacion')
        return

    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ONESIGNAL_API_KEY}"
    }
    for notification in notifications:
        hora = notification.get('hora')
        fecha_actual = dia_actual.strftime('%Y-%m-%d')
        # Concatena la fecha y la hora para formar el timestamp que OneSignal espera
        fecha_completa = f"{fecha_actual} {hora}"
        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "included_segments": ["All"],
            "contents": {
                "en": f"Tienes clase de {notification['asignatura']} en {notification['nombre_universidad']}."},
            "send_after": fecha_completa
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Notificacion - {fecha_completa} -{notification['asignatura']} en {notification['nombre_universidad']}")
        i = ServiceData()
        i.conectar_db()

        i.insert_historico_servicio(
            nombre_servicio='PUSH_NOTIFICATION',
            data=f'fecha-ejecucuion- {convert_utc_to_dominican(fecha_completa)}- '
                 f'asignatura {notification['asignatura']}- universidad {notification['nombre_universidad']}'
        )
        print(response.json())


def schedule():
    dias_espanol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miercoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sabado",
        "Sunday": "Domingo"
    }

    # Conectar a la base de datos y obtener datos (se puede ajustar según la implementación real)
    db = ServiceData()
    db.conectar_db()

    ahora_utc = datetime.now(pytz.utc)
    dia_semana_es = dias_espanol[ahora_utc.strftime("%A")]

    print(f"Hoy es {dia_semana_es}")
    data = db.obtener_asignaturas_por_dia(dia_semana_es)

    data_fecha_futura = [
        item for item in data
        if datetime.strptime(f"{ahora_utc.strftime('%Y-%m-%d')} {item['hora']}", "%Y-%m-%d %I:%M %p").replace(
            tzinfo=pytz.utc) > ahora_utc
    ]

    print(data_fecha_futura)

    schedule_notifications(data_fecha_futura, ahora_utc)

    # Calcular el delay hasta las 4:00 UTC del siguiente día (o del día actual si aún no ha pasado)
    now = datetime.now(pytz.utc)
    target = now.replace(hour=4, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    delay = (target - now).total_seconds()

    db = ServiceData()
    db.conectar_db()
    db.insert_historico_servicio(
        nombre_servicio='FECHA_EJECUCION_PUSH',
        data=f"Próxima ejecución programada en {delay} segundos, a las {target} UTC"

    )
    threading.Timer(delay, schedule).start()


# Inicia el scheduler
schedule()

# Nota: El script se mantendrá ejecutándose en un bucle gracias al threading.Timer.
