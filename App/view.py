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

"""
Menu principal
"""
while True:
    #printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
    elif int(inputs[0]) == 2:
        controller.loadFiles(cont)
    elif int(inputs[0]) == 3:
        pickUp = input("Ingrese la Community Area de la que quiere salir: ")
        dropOff = input("Ingrese la Community Area a la que quiere llegar: ")
        InitialTime = input("Ingrese el rango inferior de su horario disponible: ")
        EndTime = input("Ingrese el rango superior de su horario disponible: ")
        info = controller.getBestSchedule(cont,pickUp,dropOff,InitialTime,EndTime)
        if info[1] is not None:
            print("\nEl mejor horario para tomar el viaje es {}, el cual te tomará aproximadamente {} minutos".format(info[0],int(info[2])//60))
            print("La mejor ruta para tomar es {}\n".format("-".join(info[1])))
        else:
            print("Lo sentimos, no hay una ruta disponible en ninguno de los horarios seleccionados")
    else:
        sys.exit(0)
sys.exit(0)