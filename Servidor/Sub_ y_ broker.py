
import paho.mqtt.client as paho
from paho import mqtt
import sys

## importación de 'mysql.connector' como mysql
import mysql.connector as mysql

## importación de la clase mensaje
from Mensaje import Mensaje



'''Sentencias para tratar la suscripción.'''

# Configura el callback para diferentes eventos para ver si funciona, imprimir el mensaje, etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # suscríbase a todos los temas de la enciclopedia usando el comodín '#'
    client.subscribe("checadores", qos=1)

# imprimir a qué tema se suscribió
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


'''Sentencias para tratar la publicación.'''

#  imprimir mensaje, útil para verificar si fue exitoso
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
    # crea un archivo donde sobreescribira el mensaje mqtt
    f = open("mqtt.txt", "w")
    # se convierte en un string el msg.payload
    mensaje = str(msg.payload)
    # se elimina los dos primeros caracteres (b') y el utlimo caracter (') de la cadena
    mensaje = mensaje[2:-1]
    # se escribe el mensaje en el archivo 
    f.write(mensaje)
    # se cierra el archivo
    f.close()

    try:
        # La declaración with simplifica el manejo de excepciones al encapsular tareas comunes de preparación y limpieza  
        # ademas de cerrar en automatico el archivo
        with open('mqtt.txt') as read_file:
            # el str captado del archivo de guarda en una variable
            data = read_file.readline()

        # se inicializa el objeto mensaje para extraer los datos del json y poder usar la funciones para mysql
        # los parametros son el str del acrhivo y se incializa el objeto mysql en la clase Mensaje
        mensaje = Mensaje(data, db.cursor())

        # se comprueba si la tabla exite
        if(mensaje.comprobar_tabla()):
            # si existe se agregan los datos a la tabla
            mensaje.insertar_datos()
        else:
            # si no existe primero la cre y despues agrega los datos
            mensaje.agregar_tabla()
            mensaje.insertar_datos()

        # se realiza la confirmacion de la sentencias ejecutas del objeto mensaje a la base de datos con el objeto mysql.connect()
        db.commit()

    except FileNotFoundError:
        # sentecnias en si surge el error de FileNotFoudError se captado
        print("El archivo de mensajes mqtt no se ha creado.")
        print("La base de datos en mysql no se ha modificado")



'''Sentencias para conectarse al Broker HIVEMQ'''

# usando MQTT versión 5 aquí, para 3.1.1: MQTTv311, 3.1: MQTTv31 
# userdata son datos definidos por el usuario de cualquier tipo, actualizados por user_data_set() 
# client_id es el nombre dado del cliente
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# habilite TLS para una conexión segura
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

try:
    # establecer nombre de usuario y contraseña de la credencial
    client.username_pw_set("username", "password")
    # conectarse a HiveMQ Cloud en el puerto 8883 (predeterminado para MQTT MQTT v3.1)
    client.connect("URL", 8883)
except:
    print("No se pudo conectar al Broker MQTT.")
    print("Cerrando programa.")
    sys.exit()

# los callbacks de la siguientes, dan inicio a las funciones ademas de resguarda de nuevo la información para cada loop 
client.on_subscribe = on_subscribe
client.on_message = on_message


'''Sentencias para conectarse a la base de datos MYSQL'''

try:
## para conectar con la base de datos requrimos del metodo connect()
## requiere 4 parametros 'host', 'user', 'passwd', 'database'
    db = mysql.connect(
        host = "localhost",
        user = "Wick-Tac",
        passwd = "password",
        database = "Checadores_de_transporte"
    )

except:
    print("No se pudo conectar a la base de datos.")
    print("Cerrando programa.")
    sys.exit()



'''Sentencias para realizar loop a todo el programa'''

# loop_forever para la simplicidad, aquí necesitas detener el bucle manualmente
# También puedes usar Loop_start y Loop_stop
try:
    client.loop_forever()
except KeyboardInterrupt:  #precionar Crtl + C para salir
    print("\nCerrando.")