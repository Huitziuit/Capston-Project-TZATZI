'''
json del mensaje:

{
	"placa": "34353g",
	"checkpoint": {
			"nombre": "Pedro Gutierres",
			"checador": 1,
			"ruta": "Olivos",
			"camion": 567,
			"entradas": 15,
			"salidas": 3,
			"fecha": "2020-09-20 14:43:45"
			}
}
'''

## modulo para los json
import json

## importación de 'mysql.connector' como mysql
import mysql.connector as mysql

## esta clase convierte un string a un json y retorna las inf de manera mas facil
class Mensaje:

	'''constructor recibe un string y una base de datos.'''
	def __init__(self, jsonData, db):

		# instanciar el objeto mysql de forma "privada"
		self.__db = db
	
		# se le asignan cada atributo del json
		# se le pasa un string y la funcion json.loads lo trasnforma en un json para poder extraer los datos
		self.jsonPython = json.loads(jsonData)
		self.s_placa = self.jsonPython["placa"]
		self.s_nombre = self.jsonPython["checkpoint"]["nombre"]
		self.i_checador = self.jsonPython["checkpoint"]["checador"]
		self.s_ruta = self.jsonPython["checkpoint"]["ruta"]
		self.i_camion = self.jsonPython["checkpoint"]["camion"]
		self.i_pasajeros_E = self.jsonPython["checkpoint"]["entradas"]
		self.i_pasajeros_S = self.jsonPython["checkpoint"]["salidas"]
		
		self.dt_fecha = self.jsonPython["checkpoint"]["fecha"]
		# por si es necesario extaer la fecha en el tipo de dato datetime
		# self.dt_fecha = datetime.strptime(self.jsonPython["checkpoint"]["fecha"],"%d-%m-%Y %H:%M:%S") # se convierte el string a datetime
		
	'''función para agregar una tabla, depende del mensaje checador del mqtt.'''
	def agregar_tabla(self):
		
		# tipo de datos para la creación de la tabla
		placa = "PLACA VARCHAR(10)"
		nombre = "NOMBRE VARCHAR(30)"
		ruta = "RUTA VARCHAR(15)"
		camion = "CAMION INT"
		checador = "CHECADOR INT"
		pasajeros_E = "ENTRADAS INT"
		pasajeros_S = "SALIDAS INT"
	

		checkpoint = nombre+","+ruta+","+camion+","+checador+","
		sensores = pasajeros_E+","+pasajeros_S
		fecha = ",FECHA DATETIME"
		
		# nombre de la tabla
		placa = self.s_placa		
		query = "CREATE TABLE "+placa+" ("+checkpoint+sensores+fecha+")"

		# se indica la instrucción del query a la base de datos.
		self.__db.execute(query)

	'''función para insertar datos a una tabla.'''
	def insertar_datos(self):


		# nombre de la tabla
		placa = self.s_placa
		# definiendo el query
		query = "INSERT INTO "+placa+" (NOMBRE, RUTA, CAMION, CHECADOR, ENTRADAS, SALIDAS, FECHA) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		
		## almacenar valores en una variable
		values = (
					self.s_nombre,
					self.s_ruta,
					str(self.i_camion),
					str(self.i_checador),
					str(self.i_pasajeros_E),
					str(self.i_pasajeros_S),
					str(self.dt_fecha)
				)
		
		## indica la instrucción del query a la base de datos junto con los valores indicador por los atributos.
		self.__db.execute(query, values)
	
	# función para comprobar si existe la tabla del mensaje json 
	def comprobar_tabla(self):

		# Realiza la consulta de todas la tablas.
		self.__db.execute("SHOW TABLES")
		 
		# la funcion fetchall obtiene todas las filas de un resultado de consulta. Devuelve todas las filas como una lista de tuplas. 
		# Se devuelve una lista vacía si no hay ningún registro que recuperar.
		tuplas = self.__db.fetchall()

		# retorna un False si no hay ninguna tabla creada
		if( str(tuplas) != ""):
			for tablas in tuplas:
				#compruba cada una de las tablas con el numero de tabla del json del objeto
				if(str(tablas) == "('"+self.s_placa+"',)"):
					#retorna un True si existe la tabla del numero del checador del mensaje json
					return True
					
			# retorna un False si no existe la tabla (placa del mensaje JSON)
			return False
		# retorna un False si no hay ninguna tabla creada
		else: 
			return False
