"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

file = "201801-1-citibike-tripdata.csv"
initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Taxis")
    print("3- Requerimiento A")
    print("4- Requerimiento A")
    print("5- Identificar N mejores Taxis en una fecha")
    print("6- Identificar N mejores Taxis en un rango de fechas")
    print("7- Requerimiento C")
    print("8- Requerimiento C")
    print("0- Salir")
    print("*******************************************")


"""
Core
"""
while True:
    printMenu()
    inputs = input('Seleccione una opciÃ³n para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usarÃ¡ de acÃ¡ en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        controller.loadFiles(cont)
        print('Viajes cargados: ' + str(controller.TaxisSize(cont)))
    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("\nTiempo de ejecuciÃ³n: " + str(executiontime))

    elif int(inputs[0]) == 4:
        msg = "EstaciÃ³n Base: BusStopCode-ServiceNo (Ej: 75009-10): "
        initialStation = input(msg)
        executiontime = timeit.timeit(optionFour, number=1)
        print("\nTiempo de ejecuciÃ³n: " + str(executiontime))

    elif int(inputs[0]) == 5:
        print("\nBuscando mejores taxis en una fecha: ")
        N=int(input("Ingrese el número de mejores taxis que desee ver: "))
        Date = input("Fecha (YYYY-MM-DD): ")
        best=controller.getBestNTaxisByDate(cont, Date, N):

    elif int(inputs[0]) == 6:
        print("\nBuscando mejores taxis en un rango de fechas: ")
        print('Menor Fecha: ' + str(controller.minKey(cont)))
        print('Mayor Fecha: ' + str(controller.maxKey(cont)))
        M=int(input("Ingrese el número de mejores taxis que desee ver: "))
        inicialdate = input("Fecha inicial (YYYY-MM-DD): ")
        finaldate = input("Fecha final (YYYY-MM-DD): ")
        best=controller.getBestMTaxisByRange(analyzer, inicialdate, finaldate, M)

    elif int(inputs[0]) == 7:
        rango=input("Ingrese rango de edad:")
        executiontime = timeit.timeit(optionSeven, number=1)
        print("\nTiempo de ejecuciÃ³n: " + str(executiontime))
        
    elif int(inputs[0]) == 8:
        latu = float(input("Ingrese la latitud de su ubicacion: "))
        lonu = float(input("Ingrese la longitud de su ubicacion:"))
        latd = float(input("Ingrese la latitud del sitio que desea visitar: "))
        lond = float(input("Ingrese la longitud del sitio que desea visitar: "))
        coordsu = (latu,lonu)
        coordsd = (latd,lond)
        executiontime = timeit.timeit(optionEight, number=1)

    else:
        sys.exit(0)
sys.exit(0)