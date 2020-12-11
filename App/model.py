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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import edge as e
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import graph as gr
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    analyzer = {"CompanyServices":None, 
                "CompanyTaxis":None,
                "DatesTree": None,
                "graph": None,
                "AreaInfo": None}
    
    """analyzer["CompanyServices"] = m.newMap(comparefunction=)
    analyzer["CompanyTaxis"] = m.newMap(comparefunction=)
    analyzer["DatesTree"] = om.newMap(omaptype= "RBT",
                                      comparefunction=)"""
    analyzer["graph"] = gr.newGraph(datastructure= "ADJ_LIST",
                                    directed = True,
                                    comparefunction= compareStations)
    #analyzer["AreaInfo"] = m.newMap(maptype= "CHAINING",
    #                                comparefunction= )
    return analyzer
    
# ==============================
# Funciones para agregar informacion al grafo
# ==============================

def addLine(tripfile, analyzer):
    updateGraph(tripfile,analyzer)
    
def updateGraph(analyzer, file):
    pickUpCA = file["pickup_community_area"]
    dropOffCA = file["dropoff_community_area"]
    TripDuration = file["trip_seconds"]
    StartTime = getTimeTaxiTrip(file["trip_start_timestamp"])
    if pickUpCA != "":
        addCA(analyzer, pickUpCA)
    if dropOffCA != "":
        addCA(analyzer, dropOffCA)
    if pickUpCA != dropOffCA and TripDuration != "" and pickUpCA != "" and dropOffCA != "":    
        addConnection(analyzer,pickUpCA,dropOffCA,StartTime,TripDuration)
    
    
    
def addCA(analyzer, CommunityArea):
    if not gr.containsVertex(analyzer["graph"], CommunityArea):
        gr.insertVertex(analyzer["graph"], CommunityArea)
    return analyzer
    
    
def addConnection(analyzer, CA1, CA2, startTime, TripDuration):
    edge = gr.getEdge(analyzer["graph"], CA1, CA2)
    if edge is None:
        gr.addEdge(analyzer["graph"], CA1,CA2,TripDuration)
        edge = gr.getEdge(analyzer["graph"], CA1, CA2)
    e.updateAverageWeight(analyzer["graph"],edge,startTime)
    return analyzer

# ==============================
# Funciones de consulta
# ==============================

def getBestSchedule(graph, pickUp, dropOff, InitialTime, EndTime):
    bestSchedule = InitialTime
    currentStamp = InitialTime
    bestTime = getTime(graph,pickUp,dropOff,currentStamp)
    while currentStamp != EndTime:
        currentStamp = add15(currentStamp)
        time = getTime(graph, pickUp, dropOff, currentStamp)
        if time < bestTime:
            bestSchedule = currentStamp
            bestTime = time
    return bestSchedule
        
    
    
def getTime(graph, pickUp, dropOff, currentStamp):
    ST = djk.Dijkstra(graph, pickUp)
    time = djk.distTo(ST, dropOff)
    return time
    
# ==============================
# Funciones Helper
# ==============================
def organizeData(information, origin):
    """
    Crea un diccionario con informacion sobre una estacion en particular
    Args:
        information: El diccionario que viene del archivo con toda la info sobre un viaje
        Origin: Un booleando que define si se esta arreglando la estacion de inicio o de final de un viaje en particular 
    """
    CommunityInfo = {"CommunityArea": None}

    if origin:
        CommunityInfo["CommunityArea"] = information["pickup_community_area"]
    else:
        CommunityInfo["CommunityArea"] = information["dropoff_community_area"]
    return CommunityInfo
    
def getTimeTaxiTrip(timestamp):
    taxitripdatetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.time()
    
def add15(timestamp):
    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    timestamp =datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    fifteen = timestamp + datetime.timedelta(minutes=15)
    return fifteen.time()
# ==============================
# Funciones de Comparacion
# ==============================
def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1