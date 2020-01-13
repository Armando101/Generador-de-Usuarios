import requests
import threading 	# Módlo para hacer threads

from concurrent.futures import ThreadPoolExecutor


def get_request(event):
	response = requests.get('https://randomuser.me/api/')
	if response.status_code == 200:
		
		results = response.json().get('results')
	return results

def get_name(results):
	name = results[0].get('name').get('first')
	return name

def get_lastname(results):
	lastname = results[0].get('name').get('last')
	return lastname

def get_email(results):
	email = results[0].get('email')
	return email

def get_country(results):
	country = results[0].get('location').get('country')
	return country

def get_age(results):
	age = results[0].get('dob').get('age')
	return age

def get_user(event):
	dic = {}

	try:
		results = get_request(event)
		event.set()

		# Detenemos el programa para evitar asignaciones antes de tiempo
		event.wait()
		
		# Mandamos llamar las funciones
		name = get_name(results)

	except:
		return
	lastname = get_lastname(results)
	email = get_email(results)
	country = get_country(results)
	age = get_age(results)

	# Creamos el diccionario
	dic['name'] = name
	dic['lastname'] = lastname
	dic['email'] = email
	dic['age'] = age

	print(dic)
	return dic

def write_users(event, file):
	file = open("users.csv", "a")
	user = get_user(event)
	file.write(f"{user['name']},{user['lastname']},{user['email']},{user['age']}\n")
	file.close()


# target recibe como parámetro aquella función que queremos ejecutar de manera concurrente

if __name__ == '__main__':
	
#	for _ in range(0,20):
#	 Llamada secuencial
#		get_user()

#	Llamdada concurrente
# 	Declaramos un evento para pausar y renudar el thread
	event = threading.Event()
	executor = ThreadPoolExecutor(max_workers=25)

	file = open("users.csv", "a")
	file.write("Nombre,Apellido,Correo,Edad\n")
	file.close()

	for _ in range(100):

#		Con threads
#		thread = threading.Thread(target = get_user, args=(event,))
#		thread.start()	# Indicamos que las instrucciones se ejecuten de manera concurrente

#		Con Pools
#		Arrancamos el pool
		executor.submit(write_users, event, file)

#	Cerraos el archivo y Apagams el pool
	executor.shutdown()
