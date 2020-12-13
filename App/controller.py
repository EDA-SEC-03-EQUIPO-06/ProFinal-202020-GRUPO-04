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

import config as cf
import os
from App import model
import datetime
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer
# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadFiles(analyzer):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename)
    return analyzer
    
def loadFile(analyzer, infofile):
 
    infofile = cf.data_dir + infofile
    input_file = csv.DictReader(open(infofile, encoding= "utf-8"),
                                delimiter = ",")
    for line in input_file:
        model.addLine(analyzer, line)

    return analyzer
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

#----------------------------
# Requerimiento 1 
#----------------------------
def universal(analyzer, n):
    Total = model.Total(analyzer)
    Pq = model.PQmaker(analyzer)
    return( Total, model.getTopN(Pq, n))
#----------------------------
# Requerimiento 2
#----------------------------

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def getBestNTaxisByDate(analyzer, Date, N):
    try:
        Date = datetime.datetime.strptime(Date, '%Y-%m-%d')
        return model.getBestNTaxisByDate(analyzer, Date.date(),N)
    except:
        return 1

def getBestMTaxisByRange(analyzer, initDate, finalDate, M):
    try:
        initDate = datetime.datetime.strptime(initDate, '%Y-%m-%d')
        finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
        return model.getBestMTaxisByRange(analyzer, initDate.date(), finalDate.date(), M)
    except:
        return 1
#----------------------------
# Requerimiento 3
#----------------------------
def getBestSchedule(analyzer, pickUp, dropOff, InitialTime, EndTime):
    InitialTime = "1111-11-11T" + InitialTime +":00.000"
    InitialTime = model.getTimeTaxiTrip(InitialTime)
    EndTime = "1111-11-11T" + EndTime +":00.000"
    EndTime = model.getTimeTaxiTrip(EndTime)
    return model.getBestSchedule(analyzer["graph"],pickUp,dropOff,InitialTime,EndTime)
    

