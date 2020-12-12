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
from DISClib.ADT import stack as st
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
        addCA(analyzer, str(int(float(pickUpCA))))
    if dropOffCA != "":
        addCA(analyzer, str(int(float(dropOffCA))))
    if pickUpCA != dropOffCA and TripDuration != "" and pickUpCA != "" and dropOffCA != "" and int(float(TripDuration))>0:    
        addConnection(analyzer,str(int(float(pickUpCA))),str(int(float(dropOffCA))),StartTime,TripDuration)
    
    
    
def addCA(analyzer, CommunityArea):
    if not gr.containsVertex(analyzer["graph"], CommunityArea):
        gr.insertVertex(analyzer["graph"], CommunityArea)
    return analyzer
    
    
def addConnection(analyzer, CA1, CA2, startTime, TripDuration):
    edge = gr.getEdge(analyzer["graph"], CA1, CA2, startTime)
    if edge is None:
        gr.addEdge(analyzer["graph"], CA1,CA2,TripDuration, startTime)
    else:
        e.updateAverageWeight(analyzer["graph"],edge,TripDuration)
    return analyzer

# ==============================
# Funciones de consulta
# ==============================

def getBestSchedule(graph, pickUp, dropOff, InitialTime, EndTime):
    bestSchedule = InitialTime
    currentStamp = InitialTime
    first = getTime(graph,pickUp,dropOff,currentStamp)
    bestTime = first[0]
    search = first[1]
    while currentStamp != EndTime:
        currentStamp = add15(currentStamp)
        time = getTime(graph, pickUp, dropOff, currentStamp)
        if time[0] < bestTime:
            bestSchedule = currentStamp
            bestTime = time[0]
            search = time[1]
    path = []
    pathTo = djk.pathTo(search, dropOff)
    if pathTo is None:
        path = None
    else:
        while not st.isEmpty(pathTo):
            edge = st.pop(pathTo)
            Com = edge["vertexA"]
            path.append(Com)
            if st.size(pathTo) == 0:
                Com2 = edge["vertexB"]
                path.append(Com2)
    return bestSchedule,path,bestTime
    
def getTime(graph, pickUp, dropOff, currentStamp):
    ST = djk.Dijkstra(graph, pickUp, currentStamp)
    time = djk.distTo(ST, dropOff)
    return time,ST
    
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