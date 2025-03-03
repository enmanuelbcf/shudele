from fastapi import FastAPI, APIRouter
import httpx
import asyncio
import threading
from datetime import datetime
from ServicesDataBases.Service import ServiceData
from datetime import datetime
from contextlib import asynccontextmanager
from typing import List

from Model.app_models import Notificacion

# 🔹 Reemplaza con tus credenciales de OneSignal
ONESIGNAL_APP_ID = "ebb2b31d-1769-4f6e-8572-7b238fb961a6"
ONESIGNAL_API_KEY = "os_v2_app_5ozlghixnfhw5blspmry7olbuzq3n3rrcsiuznmeh6g77fwsc3x67xsj7lqtku7znyla5ykxfu5tl7m2kji6trihgyhsnqytxnmfoea"
lista_datos=None
primer_ejecucion = False

# 🔹 Lista de notificaciones programadas
notificaciones_programadas = []




# 🔹 Función para enviar notificación a OneSignal
async def enviar_notificacion(asignatura, universidad):
    url = "https://api.onesignal.com/notifications"
    headers = {
        "Authorization": f"Key {ONESIGNAL_API_KEY}",
        "accept": "application/json",
        "content-type": "application/json",
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "contents": {"en": f'!Uff! Emely acuerdate de la asignatura {asignatura} en {universidad} !A CORRER LOS LAKERS!'},
        "included_segments": ["All"],  # Enviar a todos los usuarios registrados
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.json()



def existe_push():
    # Obtener la fecha y hora actual
    global proxima_hora
    ahora = datetime.now()
    hora_actual = ahora.time()  # Solo extraer la hora actual

    # Diccionario de días en español
    dias_espanol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miercoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sabado",
        "Sunday": "Domingo"
    }

    # Obtener el nombre del día traducido
    dia_semana_es = dias_espanol[ahora.strftime("%A")]

    print(f"Hoy es {dia_semana_es}")

    # Conectar con la base de datos y obtener asignaturas del día actual
    db = ServiceData()
    db.conectar_db()
    data = db.obtener_asignaturas_por_dia(dia_semana_es)  # Usa el día en español

    # Verificar si hay datos antes de continuar
    if not data:
        print("📌 No hay asignaturas programadas para hoy.")
        proxima_hora = None
    else:

        # Filtrar solo las asignaturas con horas futuras
        asignaturas_futuras = []

        for item in data:
            try:
                # Extraer solo la hora de la asignatura
                hora_asignatura = datetime.strptime(item['hora'], "%I:%M %p").time()

                # Comparar solo la hora
                if hora_asignatura > hora_actual:
                    item['hora_time'] = hora_asignatura
                    asignaturas_futuras.append(item)
            except ValueError as e:
                print(f"⚠ Error en la conversión de hora ({item['hora']}): {e}")

        # Si hay asignaturas futuras, seleccionar la más próxima a la hora actual
        if asignaturas_futuras:
            proxima_hora = min(
                asignaturas_futuras,
                key=lambda x: abs(
                    (datetime.combine(ahora.date(), x['hora_time']) - ahora).total_seconds()
                )
            )

            # Calcular los segundos faltantes
            diferencia = datetime.combine(ahora.date(), proxima_hora['hora_time']) - ahora
            segundos_faltantes = diferencia.total_seconds()


            return {
                'segundos_faltantes': segundos_faltantes,
                'asignatura': proxima_hora['asignatura'],
                'nombre_universidad':proxima_hora['nombre_universidad']
            }

        else:
            return None


async def send_push():
    global lista_datos
    global primer_ejecucion

    if lista_datos is None:
        lista_datos = existe_push()
        primer_ejecucion = False

    print(lista_datos)

    if lista_datos:
        print(f'DENTRO DE LA FUNCION - {lista_datos}')
        delay = lista_datos['segundos_faltantes']
        if primer_ejecucion:
            print(f'DENTRO DEL SEND - {lista_datos}')

            # Ejecutar la tarea asíncrona
            await enviar_notificacion(lista_datos['asignatura'], lista_datos['nombre_universidad'])
            print(f"📢 Notificación enviada: {lista_datos['asignatura']} en {lista_datos['nombre_universidad']}")
            lista_datos = None
    else:
        delay = 7200
        primer_ejecucion = False

    primer_ejecucion = True
    print(primer_ejecucion)
    print(f"⏳ Siguiente ejecución en {delay} segundos")

    # Usamos `asyncio.sleep` para hacer la espera sin bloquear el bucle de eventos
    await asyncio.sleep(delay)  # Esperar el tiempo en vez de usar un Timer
    await send_push()  # Ejecutar nuevamente la función

# Iniciar el bucle de eventos principal

