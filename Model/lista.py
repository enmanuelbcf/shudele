universities = [
    "UAPA", "Universidad Abierta para adultos", "foto base64", "Inglés", "Martes", "08:00 AM", "10:00 AM", "A101",
    "UAPA", "Universidad Abierta para adultos", "foto base64", "Matemáticas", "Martes", "08:00 AM", "10:00 AM", "A101"
]

import json

universities = [
    ["UAPA", "Universidad Abierta para Adultos", "foto base64", "Inglés", "Martes", "08:00 AM", "10:00 AM", "A101"],
    ["UAPA", "Universidad Abierta para Adultos", "foto base64", "Matemáticas", "Martes", "10:00 AM", "12:00 PM",
     "A102"],

    ["UASD", "Universidad Autónoma de Santo Domingo", "foto base64", "Historia", "Miércoles", "02:00 PM", "04:00 PM",
     "B203"],
    ["UASD", "Universidad Autónoma de Santo Domingo", "foto base64", "Filosofía", "Jueves", "08:00 AM", "10:00 AM",
     "B101"],

    ["PUCMM", "Pontificia Universidad Católica Madre y Maestra", "foto base64", "Programación", "Lunes", "02:00 PM",
     "04:00 PM", "C305"],
    ["PUCMM", "Pontificia Universidad Católica Madre y Maestra", "foto base64", "Redes", "Viernes", "09:00 AM",
     "11:00 AM", "C102"],

    ["INTEC", "Instituto Tecnológico de Santo Domingo", "foto base64", "Cálculo", "Martes", "08:00 AM", "10:00 AM",
     "D201"],
    ["INTEC", "Instituto Tecnológico de Santo Domingo", "foto base64", "Física", "Jueves", "02:00 PM", "04:00 PM",
     "D305"],
]

result = {}

for uni in universities:
    acronym, name, logo, subject, day, start, end, room = uni

    if acronym not in result:
        result[acronym] = {
            "acronym": acronym,
            "name": name,
            "logo": logo,
            "subjects": []
        }

    result[acronym]["subjects"].append({
        "name": subject,
        "day": day,
        "start": start,
        "end": end,
        "room": room
    })

# Convertimos el diccionario en una lista
university_list = list(result.values())

# Mostramos el JSON
print(json.dumps(university_list, indent=4))
