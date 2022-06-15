# Para usar OpenCV en raspberry 
Debe instalar  el OS de Raspberry **Buster** descargando el archivo comprimido [2021-05-07-raspios-buster-armhf.zip](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip), ya que esta versión del OS puede ejecutar OpenCV de forma estable. Una vez descargado, extraemos el archivo.

Para instalar el OS en el raspberry es necesario descargar el programa [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

Ahora abrimos el programa de Raspberry Pi Imager: 
1. Seleccionamos la opción CHOOSE OS, lo que desplegara un menú en donde seleccionaremos la opción USE CUSTOM lo que nos abrira un axplorador de archivos y podremos buscar el archivo que extrajimos (EL OS BUSTER ).
2. Conectamos la memoria micro sd y en el menú principal de Raspberry Pi Imager seleccionamos CHOOSE STORAGE y seleccionamos nuestra memoria micro sd.
3. Finalmente despues del proceso de instalacion del OS en la memoria micro sd, la extraemeos y conectamos a la raspberry.

Despues de ejecutar con exito el OS en la raspberry y de conectarla a internet intalamos OpenCV con los siguientes comandos.

```
sudo apt-get update

sudo apt-get install python3-opencv

sudo apt-get install libqt4-test python3-sip python3-pyqt5 libqtgui4 libjasper-dev libatlas-base-dev -y

pip3 install opencv-contrib-python==4.1.0.25

sudo modprobe bcm2835-v4l2 
```
---
Sin embargo, aún falta habilitar la interfaz de la cámara en las preferencias de configuración de raspberry, ya que por defecto está deshabilitada Para habilitar y comprobar que la la cámara en la raspberry funciona puedes ver el siguiente[tutorial](https://www.youtube.com/watch?v=tHjwx2AQHxU&ab_channel=DataSlayer)
