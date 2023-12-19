from datetime import datetime

def hacer_pregunta(pregunta, ejemplo, tipo='texto'):
    print(pregunta)
    if ejemplo:
        print(f"Por ejemplo, puedes responder: '{ejemplo}'")
    respuesta = ""
    while not respuesta:
        respuesta = input("Tu respuesta: ")
        if tipo == 'si_no' and respuesta.lower() not in ['sí', 'si', 'no']:
            print("Por favor, responde con 'sí' o 'no'.")
            respuesta = ""
    return respuesta

def realizar_cuestionario():
    puntaje = 0
    print("Vamos a realizar algunas preguntas. Te daré ejemplos de cómo responder.")

    # Orientación Temporal
    año_actual = str(datetime.now().year)
    mes_actual = datetime.now().strftime("%B")
    dia_actual = str(datetime.now().day)
    respuesta_año = hacer_pregunta("¿Qué año es?", año_actual)
    if respuesta_año == año_actual:
        puntaje += 1
    respuesta_mes = hacer_pregunta("¿Qué mes es?", mes_actual)
    if respuesta_mes.lower() == mes_actual.lower():
        puntaje += 1
    respuesta_dia = hacer_pregunta("¿Qué día del mes es hoy?", dia_actual)
    if respuesta_dia == dia_actual:
        puntaje += 1

    # Orientación en el Espacio
    respuesta_espacio1 = hacer_pregunta("¿Estás en una casa o en un hospital?", "casa o hospital")
    if respuesta_espacio1.lower() in ["casa", "hospital"]:
        puntaje += 1
    respuesta_espacio2 = hacer_pregunta("¿Estás dentro o fuera de un edificio?", "sí o no", 'si_no')
    if respuesta_espacio2.lower() in ["sí", "si", "no"]:
        puntaje += 1

    # Memoria Inmediata
    numero_para_recordar = "123"
    print(f"Recuerda este número: {numero_para_recordar}")
    hacer_pregunta("¿Puedes decirme tu nombre completo?", "Juan Pérez")
    respuesta_numero = hacer_pregunta("¿Cuál era el número que te pedí recordar?", "123")
    if respuesta_numero == numero_para_recordar:
        puntaje += 1

    # Atención y Cálculo
    respuesta_calculo = hacer_pregunta("¿Cuánto es 2+3?", "5")
    if respuesta_calculo == "5":
        puntaje += 1

    # Lenguaje
    respuesta_animal = hacer_pregunta("Nombra un animal.", "perro, gato, elefante")
    if respuesta_animal.strip():
        puntaje += 1

    # Repetición de Frases Simples
    frase_para_repetir = "El cielo es azul"
    respuesta_frase = hacer_pregunta(f"Por favor, repite: '{frase_para_repetir}'", frase_para_repetir)
    if respuesta_frase.lower() == frase_para_repetir.lower():
        puntaje += 1

    # Reconocimiento de Objetos Comunes
    print("Imagina una silla de madera con cuatro patas y un respaldo.")
    respuesta_objeto = hacer_pregunta("¿Qué objeto es?", "silla")
    if respuesta_objeto.lower().strip() == "silla":
        puntaje += 1

    # Reconocimiento de Colores Básicos
    print("Imagina una tarjeta de color azul brillante.")
    respuesta_color = hacer_pregunta("¿De qué color es la tarjeta que te pedí imaginar?", "azul")
    if respuesta_color.lower() == "azul":
        puntaje += 1

    # Respuesta a Preguntas de Sí/No
    es_de_dia = "sí" if datetime.now().hour < 18 and datetime.now().hour > 6 else "no"
    respuesta_dia = hacer_pregunta("¿Es de día ahora?", es_de_dia, 'si_no')
    if respuesta_dia.lower() == es_de_dia:
        puntaje += 1

    return puntaje

# Ejecutar el cuestionario
puntaje_total = realizar_cuestionario()
print(f"\nTu puntuación en el cuestionario es: {puntaje_total}")
