from datetime import datetime
from ServicesDataBases.Service import ServiceData

# Obtener la fecha y hora actual
ahora = datetime.now()
hora_actual = ahora.time()  # Solo extraer la hora actual

# Diccionario de días en español
dias_espanol = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Obtener el nombre del día traducido
dia_semana_es = dias_espanol[ahora.strftime("%A")]

print(f"Hoy es {dia_semana_es}")

# Conectar con la base de datos y obtener asignaturas del día actual
db = ServiceData()
db.conectar_db()
data = db.obtener_asignaturas_por_dia('Martes')  # Usa el día en español

# Verificar si hay datos antes de continuar
if not data:
    print("📌 No hay asignaturas programadas para hoy.")
    proxima_hora = None
else:
    print("📚 Asignaturas del día:", data)

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

        # Mostrar resultados
        print(f"📌 Próxima asignatura: {proxima_hora['asignatura']} en {proxima_hora['nombre_universidad']}")
        print(f"📅 Hora programada: {proxima_hora['hora']} ({proxima_hora['hora_time']})")
        print(f"⏳ Segundos faltantes: {segundos_faltantes:.0f} segundos")
    else:
        print("📌 No hay más asignaturas futuras para hoy.")
        proxima_hora = None
