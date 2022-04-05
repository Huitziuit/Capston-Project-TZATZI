from pickle import TRUE
import time
import paho.mqtt.client as paho
from paho import mqtt
import random

# configurar devoluciones de llamada para diferentes eventos para ver si funciona, imprimir el mensaje, etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# con esta devolución de llamada puede ver si su publicación fue exitosa
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# imprimir a qué tema se suscribió
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# usando MQTT versión 5 aquí, para 3.1.1: MQTTv311, 3.1: MQTTv31 
# userdata son datos definidos por el usuario de cualquier tipo, actualizados por user_data_set() 
# client_id es el nombre dado del cliente
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# habilite TLS para una conexión segura
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# establecer nombre de usuario y contraseña
client.username_pw_set("Wick-Tac", "@Fj2193037519")

# conectarse a HiveMQ Cloud en el puerto 8883 (predeterminado para MQTT MQTT v3.1)
client.connect("e681dce206654d94890b6310d899142f.s1.eu.hivemq.cloud", 8883)


client.on_publish = on_publish


# ***** INICIO DEL CODIGO PARA SIMULAR LOS DATOS Y MENSAJE DEL JSON QUE SE PUBLICARA,
#       SI YA CUENTA CON UN MENSAJE JSON PARA MANDAR PUEDE COMENTAR LAS LINES SIGUIENES Y INICIAR LA VARIABLE (mensaje) PARA SUS FINES ********

try:

# una sola publicación, esto también se puede hacer en bucles, etc.
    
    #bandera  = 0
    #while(bandera <10):
    while(True):

        # Variables simuladas
        #placa = '"placa": "AAA0003"'

        placa ='"placa": "AAA000'+str(random.randint(1,3))+'"'
        checador = '"checador": '+str(random.randint(0,15))
        camion = '"camion": '+str(random.randint(0,30))

        entradas_n = random.randint(0, 20)
        entradas = '"entradas": '+str(entradas_n)
        salidas = '"salidas": '+str(random.randint(0, int(entradas_n)))

        fecha = '"fecha": '+'"'+(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))+'"'

        # mensaje json
        mensaje = ('{'+placa+',"checkpoint": {"nombre": "Pedro Gutierres",'+checador+',"ruta": "Olivos",'+camion+','+entradas+','+salidas+','+fecha+'}}')
        print(mensaje)	


        client.publish('checadores', payload=mensaje, qos=0)
        #bandera +=1
        time.sleep(1)

except KeyboardInterrupt:  #precionar Crtl + C para salir
    print("\nCerrando.")


# ***** FIN DE LAS LINEAS DE CODIGO PARA SIMULAR DATOS, INICIE UN OBJETO (mensaje) PARA SUS FINES Y DESCOMENTE LA SIGUIENTE Y ULTIMA LINEA DE CODIGO ************

# mensaje = "TU MENSAJE json"

# una sola publicación, esto también se puede hacer en bucles, etc.

#try:
#    client.publish("topic", payload="mensaje", qos=1)
#except KeyboardInterrupt:  #precionar Crtl + C para salir
#    print("\nCerrando.")