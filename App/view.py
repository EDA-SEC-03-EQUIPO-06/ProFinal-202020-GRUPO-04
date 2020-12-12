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
from DISClib.ADT import minpq as pq
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

def printBestTaxis(qeue, N):
    i=0
    while i<N and not pq.isEmpty(qeue):
        taxi=pq.delMin(qeue)
        print("\n------ "+str(i+1)+" ------")
        print("⚛︎ Taxi ID: {0}".format(taxi["id"]))
        print("⚛︎ Puntaje: {0}".format(round(taxi["points"],2)))
        i+=1
    print("\n\nACLARACIÓN: Si aparecen menos taxis de los esperados es porque no hay {0} taxis en esa fecha".format(N))
"""
Core
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usarÃ¡ de acÃ¡ en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        controller.loadFiles(cont)
        print('Viajes cargados: ' + str(controller.TaxisSize(cont)))
    
    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        print("\nBuscando mejores taxis en una fecha: ")
        print('Menor Fecha: ' + str(controller.minKey(cont)))
        print('Mayor Fecha: ' + str(controller.maxKey(cont)))
        a=False
        while a==False:
            try:
                N=int(input("Ingrese el número de mejores taxis que desee ver: "))
                a=True
            except:
                pass
        Date = input("Fecha (YYYY-MM-DD): ")
        bestN=controller.getBestNTaxisByDate(cont, Date, N)
        if bestN==1:
            print("El formato de fechas dado es inválido. Vuélvalo a intentar")
        elif bestN==0 or pq.isEmpty(bestN):
            print("No se encontraron taxis en esa fecha")
        else:
            print("\nLa lista de los mejores {0} taxis con sus respectivos puntos es: ".format(N))
            printBestTaxis(bestN,N)
            

    elif int(inputs[0]) == 6:
        print("\nBuscando mejores taxis en un rango de fechas: ")
        print('Menor Fecha: ' + str(controller.minKey(cont)))
        print('Mayor Fecha: ' + str(controller.maxKey(cont)))
        a=False
        while a==False:
            try:
                M=int(input("Ingrese el número de mejores taxis que desee ver: "))
                a=True
            except:
                pass
        inicialdate = input("Fecha inicial (YYYY-MM-DD): ")
        finaldate = input("Fecha final (YYYY-MM-DD): ")
        bestM=controller.getBestMTaxisByRange(cont, inicialdate, finaldate, M)
        if bestM==1:
            print("\nEl formato de fechas dado es inválido. Vuélvalo a intentar")
        elif bestM==0 or pq.isEmpty(bestM):
            print("\nNo se encontraron taxis en ese rango de fechas.")
        else:
            print("\nLa lista de los mejores {0} taxis con sus respectivos puntos es: ".format(M))
            printBestTaxis(bestM,M)
    elif int(inputs[0]) == 7:
        pass
    elif int(inputs[0]) == 8:
        pass

    else:
        sys.exit(0)
sys.exit(0)