#dependencias 
import cv2
import time
import paho.mqtt.publish as publish
import paho.mqtt.client as paho
from paho import mqtt
import time
import random

#Creo cliente para broker privado-------------
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
client.username_pw_set("tu usuario", "tu contraseña")

# conectarse a HiveMQ Cloud en el puerto 8883 (predeterminado para MQTT MQTT v3.1)
client.connect("e681dce206654d94890b6310d899142f.s1.eu.hivemq.cloud", 8883)

client.on_publish = on_publish

#---------------------------------------------



# el objeto cap servira para usar OpenCV
cap = cv2.VideoCapture(0)

# Metodo detector de QR
detector = cv2.QRCodeDetector()

#Variable auxiliar para evitar redundancia en mensajes repetidos
aux=""
#loop infinito para que la camara busque informacion en lo que ve
while True:
    
    # Metodo para obtener una imagen apartir de un QR 
    _, img = cap.read()
    
    # Este metodo determina las coordenadas del QR dentro de la imagen
    data, bbox, _ = detector.detectAndDecode(img)
    
    # Donde sea detectado el QR se dibuja una caja azul y a un lado los datos que este QR representa
    if(bbox is not None):
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 0), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 250, 120), 2)
        
        # A cntinuacion, la seccion de codigo encargada de segun el contenido QR enviar al servidor el mensaje correspondiente
        # Si se detecta al gun QR entonces 
        if data:
            #print("data found: ", data) #Util durante las pruebas 
            
            # Comprobamos que la informacion no fue ya detactada con la variable aux
            # Los metodos publish.single sirven en caso de que no se cuente con un cluster privado 
            # en ese caso se puede hacer una publicacion simple que consta del topic, el mensaje, y el host,
            # ademas si se usa un cluster publico se pueden omitir las lineas de codigo de la 10 a la 38 pero este tipo de clusters cambian de host muy recurrentemente por lo que no se recomienda

            if data!=aux: 
                if data == 'camion1':
                    print("Notificando por mqtt camion 1")
                    
                    #publish.single("huitzi/exampl", "camion 1 detectado en la estacion A", hostname="18.197.171.34")
                    
                    # Variables de camion
                    placa = '"placa": '+'"AAA0001"'
                    checador = '"checador": 1'
                    camion = '"camion": 23'

                    entradas_n = random.randint(0, 20)
                    entradas = '"entradas": '+str(entradas_n)
                    salidas = '"salidas": '+str(random.randint(0, int(entradas_n)))

                    fecha = '"fecha": '+'"'+(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))+'"'

                    # mensaje json
                    mensaje = ('{'+placa+',"checkpoint": {"nombre": "Jacobo Alejandro",'+checador+',"ruta": "Lerma",'+camion+','+entradas+','+salidas+','+fecha+'}}')
                    print(mensaje)	

                    #Notifico al cluster 
                    client.publish('checadores', payload=mensaje, qos=0)
                    
                
                if data == 'camion2':
                    print("Notificando por mqtt camion 2")
                    publish.single("huitzi/exampl", "camion 2 detectado en la estacion A", hostname="18.197.171.34")
                
                    # Variables de camion
                    placa = '"placa": '+'"AAA0002"'
                    checador = '"checador": 1'
                    camion = '"camion": 71'

                    entradas_n = random.randint(0, 20)
                    entradas = '"entradas": '+str(entradas_n)
                    salidas = '"salidas": '+str(random.randint(0, int(entradas_n)))

                    fecha = '"fecha": '+'"'+(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))+'"'

                    # mensaje json
                    mensaje = ('{'+placa+',"checkpoint": {"nombre": "Erick Huitziuit",'+checador+',"ruta": "Cuajimalpa",'+camion+','+entradas+','+salidas+','+fecha+'}}')
                    print(mensaje)

                    #Notifico al cluster 
                    client.publish('checadores', payload=mensaje, qos=0)
                    
                if data == 'camion3':
                    print("Notificando por mqtt camion 3")
                    publish.single("huitzi/exampl", "camion 3 detectado en la estacion A", hostname="18.197.171.34")
                    # Variables de camion
                    placa = '"placa": '+'"AAA0003"'
                    checador = '"checador": 1'
                    camion = '"camion": 99'

                    entradas_n = random.randint(0, 20)
                    entradas = '"entradas": '+str(entradas_n)
                    salidas = '"salidas": '+str(random.randint(0, int(entradas_n)))

                    fecha = '"fecha": '+'"'+(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))+'"'

                    # mensaje json
                    mensaje = ('{'+placa+',"checkpoint": {"nombre": "Alfredo Garcia",'+checador+',"ruta": "Cuajimalpa",'+camion+','+entradas+','+salidas+','+fecha+'}}')
                    print(mensaje)

                    #Notifico al cluster 
                    client.publish('checadores', payload=mensaje, qos=0)
                
                aux=data
                
                
        
            
    # Muestra lo que la camara ve en tiempo real
    cv2.imshow("code detector", img)
    
    # la tecla "q" detiene el programa
    if(cv2.waitKey(1) == ord("q")):
        break
    
    # cuando se detiene el programa se cierran todas las ventanas que este crea 
cap.release()
cv2.destroyAllWindows()
