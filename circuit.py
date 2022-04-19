import requests
import threading
from requests import RequestException
from circuitbreaker import circuit, CircuitBreakerMonitor

#intentos
FAILURES = 5

#Metodo de respuesta cuando termina los intentos
def fallbackempresa(empresa):
    print("no se logro conexion para crear empresa {} en {} intentos ".format(empresa["nombre"],FAILURES),)

#Metodo de respuesta cuando termina los intentos
def fallbackestudiante(estudiante):
    print("no se logro conexion para crear estudiante {} en {} intentos".format(estudiante["nombre"],FAILURES))

#metodo con la configuracion de circuit breaker
@circuit(failure_threshold=FAILURES,fallback_function=fallbackestudiante,expected_exception = RequestException)
def crear_estudiante(estudiante):
    
    
    url = 'http://httpstat.us/401'
    response = requests.get(url)
    print(response)
    response.raise_for_status()
    #logica de negocio
    print("Estudiante creado {} {}".format(estudiante["nombre"],response.text))
    #//
   
    return response

#metodo con la configuracion de circuit breaker
@circuit(failure_threshold=FAILURES,fallback_function=fallbackempresa,expected_exception = RequestException)
def crear_empresa(empresa):

    url = 'http://httpstat.us/200'
    response = requests.get(url)
    print(response)
    response.raise_for_status()
    #logica de negocio
    print("Empresa creada {} {}".format(empresa["nombre"],response.text))
    #//
    return response

#def print_summary():
#    for x in CircuitBreakerMonitor.get_circuits(): 
#        msg = "{} circuit state: {}. Time till open: {}"
#        print(msg.format(x.name, x.state, x.open_remaining))


#ejecuta el circuito cuantas veces se configure en failure_threshold
def run_circuit(func,obj):
    totry = True
    while(totry):
          try: 
            result = func(obj)
            totry = False if result or result is None else True
          except: 
            pass
          #print_summary() 

#Datos
estudiante ={}
estudiante["nombre"] = "Mario"
empresa ={}
empresa["nombre"] = "Home Center"

#ejecucion en paralelo
#hiloeestudiante = threading.Thread(target=run_circuit,args=(crear_estudiante,estudiante))
#hiloeempresa = threading.Thread(target=run_circuit,args=(crear_empresa,empresa))

#lanzar los hilos
#hiloeestudiante.start()
#hiloeempresa.start()

#esperar los hilos o sincronizarlos
#hiloeempresa.join()
#hiloeestudiante.join()

run_circuit(crear_estudiante,estudiante)
run_circuit(crear_empresa,empresa)

print("Fin programa")
