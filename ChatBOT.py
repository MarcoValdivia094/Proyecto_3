import json
import random

ARCHIVO_RESPUESTAS = "intenciones.json"

# Las "Intenciones" se refieren al objetivo del mensaje del usuario.
# Ejemplo: si el usuario escribe "hola", la intención es "saludo".
# Si escribe "adiós", la intención es "despedida".
# Cada intención tiene:
#   - Palabras clave que la activan
#   - Respuestas posibles que el chatbot puede dar

# Intentamos cargar las intenciones guardadas desde un archivo JSON.
# Si el archivo no existe, se crean intenciones iniciales (saludo y despedida).
try:
    with open(ARCHIVO_RESPUESTAS, "r") as f:
        intenciones = json.load(f)
except FileNotFoundError:
    intenciones = {
        "saludo": {
            "palabras": ["hola", "buenas", "qué tal", "hey"],
            "respuestas": [
                "¡Hola! Qué gusto saludarte.",
                "Hey, ¿cómo estás?",
                "¡Buenas! ¿Qué tal tu día?"
            ]
        },
        "despedida": {
            "palabras": ["adios", "bye", "nos vemos", "hasta luego"],
            "respuestas": [
                "Adiós, ¡cuídate mucho!",
                "Nos vemos pronto.",
                "Bye, que tengas un buen día."
            ]
        }
    }

# Función para guardar las intenciones en el archivo JSON.
# Esto permite que el chatbot recuerde lo que ha aprendido incluso después de cerrar el programa.
def guardar_intenciones():
    with open(ARCHIVO_RESPUESTAS, "w") as f:
        json.dump(intenciones, f, indent=4)

# Función para detectar la intención de un mensaje.
# Recorre todas las intenciones y sus palabras clave.
# Si alguna palabra clave está dentro del mensaje del usuario, devuelve esa intención.
def detectar_intencion(mensaje):
    mensaje = mensaje.lower()
    for nombre, datos in intenciones.items():
        for palabra in datos["palabras"]:
            if palabra in mensaje:
                return nombre
    return None

# Función principal del chatbot.
# Aquí se maneja la interacción con el usuario.
def chatbot():
    print("🤖 Hola, soy tu chatbot con aprendizaje. Escribe 'salir' para terminar.")
    print("👉 También puedes escribir 'modificar intencion' para agregar palabras o respuestas a una intención existente.")
    
    while True:
        mensaje = input("Tú: ").lower()
        
        # Si el usuario escribe "salir", el chatbot termina y guarda las intenciones.
        if mensaje == "salir":
            print("Bot: Adiós, ¡nos vemos pronto!")
            guardar_intenciones()
            break
        
        # Si el usuario escribe "modificar intencion", se muestra un menú para editar intenciones existentes.
        elif mensaje == "modificar intencion":
            print("Bot: Estas son las intenciones que existen actualmente:")
            for nombre in intenciones.keys():
                print(f" - {nombre}")
            
            nombre = input("¿Cuál quieres modificar?: ").lower()
            if nombre in intenciones:
                print("Bot: ¿Quieres agregar una palabra clave o una respuesta? (palabra/respuesta)")
                tipo = input("Tú: ").lower()
                if tipo == "palabra":
                    # Mostrar palabras actuales antes de agregar una nueva
                    print(f"Bot: Actualmente las palabras clave para '{nombre}' son: {intenciones[nombre]['palabras']}")
                    nueva_palabra = input("Escribe la nueva palabra clave: ").lower()
                    intenciones[nombre]["palabras"].append(nueva_palabra)
                    print(f"Bot: ¡Listo! Ahora '{nueva_palabra}' también activará la intención '{nombre}'.")
                elif tipo == "respuesta":
                    # Mostrar respuestas actuales antes de agregar una nueva
                    print(f"Bot: Actualmente las respuestas para '{nombre}' son: {intenciones[nombre]['respuestas']}")
                    nueva_respuesta = input("Escribe la nueva respuesta: ")
                    intenciones[nombre]["respuestas"].append(nueva_respuesta)
                    print(f"Bot: ¡Perfecto! Ahora puedo responder también: '{nueva_respuesta}'.")
                guardar_intenciones()
            else:
                print("Bot: Esa intención no existe todavía.")
        
        else:
            # Detectar intención del mensaje
            intencion = detectar_intencion(mensaje)
            if intencion:
                # Responder con una frase aleatoria de la intención detectada
                print("Bot:", random.choice(intenciones[intencion]["respuestas"]))
            else:
                # Si no entiende, ofrece aprender una nueva intención
                print("Bot: No entiendo. ¿Quieres enseñarme una nueva intención?")
                opcion = input("Tú (sí/no): ").lower()
                if opcion == "sí":
                    nueva_intencion = input("¿Cómo se llama esta intención?: ").lower()
                    nueva_palabra = input("Escribe una palabra clave que la active: ").lower()
                    nueva_respuesta = input("Escribe una respuesta que debería dar: ")
                    
                    # Crear la intención si no existe
                    if nueva_intencion not in intenciones:
                        intenciones[nueva_intencion] = {"palabras": [], "respuestas": []}
                    intenciones[nueva_intencion]["palabras"].append(nueva_palabra)
                    intenciones[nueva_intencion]["respuestas"].append(nueva_respuesta)
                    
                    print("Bot: ¡Gracias! Ahora ya sé cómo responder a esa intención.")
                    guardar_intenciones()
                else:
                    print("Bot: Está bien, avísame si quieres crear una.")

# Ejecutar el chatbot
chatbot()
