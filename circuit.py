import requests
import threading
from requests import RequestException
from circuitbreaker import circuit, CircuitBreakerMonitor
FAILURES = 10

#Metodo de respuesta cuando termina los intentos
def fallbackempresa(empresa):
    print("no se logro conexion para crear empresa {} en {} intentos ".format(empresa["nombre"],FAILURES),)

#Metodo de respuesta cuando termina los intentos
def fallbackestudiante(estudiante):
    print("no se logro conexion para crear estudiante {} en {} intentos".format(estudiante["nombre"],FAILURES))

@circuit(failure_threshold=FAILURES,fallback_function=fallbackestudiante,expected_exception = RequestException)
def crear_estudiante(estudiante):
    
    #logica de negocio
    url = 'http://httpstat.us/401'
    response = requests.get(url)
    print(response)
    #//
    response.raise_for_status()
    print("Estudiante creado {} {}".format(estudiante["nombre"],response.text))
    return response


@circuit(failure_threshold=FAILURES,fallback_function=fallbackempresa,expected_exception = RequestException)
def crear_empresa(empresa):

    #logica de negocio
    url = 'http://httpstat.us/200'
    response = requests.get(url)
    print(response)
    #//
    response.raise_for_status()
    print("Empresa creada {} {}".format(empresa["nombre"],response.text))
    return response

#def print_summary():
#    for x in CircuitBreakerMonitor.get_circuits(): 
#        msg = "{} circuit state: {}. Time till open: {}"
#        print(msg.format(x.name, x.state, x.open_remaining))


def run_circuit(func,obj):
    totry = True
    while(totry):
          try: 
            result = func(obj)
            totry = False if result or result is None else True
          except: 
            pass
          #print_summary() 


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

#esperar los hilos o soncronizarlos
#hiloeempresa.join()
#hiloeestudiante.join()

run_circuit(crear_estudiante,estudiante)
run_circuit(crear_empresa,empresa)

print("Fin programa")
