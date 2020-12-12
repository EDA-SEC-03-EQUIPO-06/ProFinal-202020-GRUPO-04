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


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n0- Inicializar Catálogo")
    print("1- Cargar Archivos")
    print("2- Descubrir productoras de cine")
    print("3- Conocer a un director")
    print("4- Conocer a un actor")
    print("5- Entender un género cinematográfico")
    print("6- Encontrar películas por país")
    print("7- Salir")




def optionTwo():
    print("\nCargando información ....")
    controller.loadFiles(cont)



def optionThree():
    """
    Requerimento 1
    """
    r= (controller.universal(cont, n))
    print("\nLos resultados encrontados son: \n")
    print(r[0])
    print("\n El top compañias por numero de taxis es: \n")
    print(r[1][0])
    print("\n El top compañias por numero de servicios es: \n")
    print(r[1][1])
"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        n = int(input("Escriba el numero de compañias incluidas en el Ranking: "))
        executiontime = timeit.timeit(optionThree, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))



    else:
        sys.exit(0)