import threading
from time import daylight

import schedule
import pytz
import requests
import json
from datetime import datetime, timedelta

from ServicesDataBases.Service import ServiceData
from utlis.funciones_utlis import convert_utc_to_dominican




def schedule_notifications(notifications, dia_actual):
    parametro = ServiceData()
    parametro.conectar_db()
    ONESIGNAL_APP_ID = "ebb2b31d-1769-4f6e-8572-7b238fb961a6"
    ONESIGNAL_API_KEY = "os_v2_app_5ozlghixnfhw5blspmry7olbuzq3n3rrcsiuznmeh6g77fwsc3x67xsj7lqtku7znyla5ykxfu5tl7m2kji6trihgyhsnqytxnmfoea"

    if len(notifications)  < 1:
        print(f'dia - {dia_actual} - no hay notificacions')
        return

    url = "https://onesignal.com/api/v1/notifications"


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ONESIGNAL_API_KEY}"
    }
    minutos_resta =  parametro.obtener_parametro_por_id('MINUTOS-PUSH-NOTIFICATION')

    min = minutos_resta['value']

    for notification in notifications :
        hora = notification['hora']
        hora_min = hora - timedelta(minutes=int(min))
        hora_dt = hora_min.strftime('%H:%M:%S')
        fecha_actual = dia_actual.strftime('%Y-%m-%d')

        # Concatena la fecha y la hora para formar el timestamp que OneSignal espera
        fecha_completa = f"{fecha_actual} {hora_dt}"
        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "included_segments": ["All"],
            ''
            "contents": {
                "en": f"Tienes clase de {notification['asignatura']} en"
                      f" {notification['nombre_universidad']} [{convert_utc_to_dominican(notification['hora'])[11:]}" 
                      f" - {convert_utc_to_dominican(notification['hora_fin'])[11:]}]"
                      f".!A CORRER LOS LAKERS!!!"},
            # "send_after": fecha_completa
            "android_vibrate": True,
            "android_vibration_pattern": [100, 200, 100, 300]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Notificacion - {convert_utc_to_dominican(notification['hora'])[11:]}"
              f"-{notification['asignatura']} en {notification['nombre_universidad']}")


        if response.status_code == 200:
            hist = ServiceData()
            hist.conectar_db()

            parametro.insert_historico_servicio(
                nombre_servicio='PUSH_NOTIFICATION',
                data=f'fecha-ejecucuion- {convert_utc_to_dominican(datetime.now(pytz.utc))}'
                     f'asignatura {notification['asignatura']}- universidad {notification['nombre_universidad']}'
            )


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

    db =  ServiceData()
    db.conectar_db()

    # Conectar a la base de datos y obtener datos (se puede ajustar según la implementación real)

    ahora_utc = datetime.now(pytz.utc)

    dia_semana_es = dias_espanol[ahora_utc.strftime("%A")]

    print(f"Hoy es {dia_semana_es}")
    data = db.obtener_asignaturas_por_dia(dia_semana_es)

    # print(data)
    data_fecha_futura = []
    for item in data:
        if item['hora'] >= ahora_utc:
            data_fecha_futura.append(item)

    print(data_fecha_futura)
    schedule_notifications(data_fecha_futura, ahora_utc)

    # Calcular el delay hasta las 4:00 UTC del siguiente día (o del día actual si aún no ha pasado)
    now = datetime.now(pytz.utc)
    target = now.replace(hour=4, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    delay = (target - now).total_seconds()

    db.insert_historico_servicio(
        nombre_servicio='FECHA_EJECUCION_PUSH',
        data=f"Próxima ejecución programada en {delay} segundos, a las {target} UTC"

    )
    print(f'DELAY - {delay}')
    threading.Timer(delay, schedule).start()

