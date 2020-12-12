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
from DISClib.ADT import minpq as pq
from DISClib.DataStructures import edge as e
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import quicksort as qs
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
                "DateIndex": None,
                "graph": None}
    analyzer["CompanyServices"] = m.newMap(comparefunction=compareIds)
    analyzer["CompanyTaxis"] = m.newMap(comparefunction=compareIds)

    analyzer["DateIndex"] = om.newMap(omaptype= "RBT",
                                      comparefunction=compareDates)
    analyzer["graph"] = gr.newGraph(datastructure= "ADJ_LIST",
                                    directed = True,
                                    comparefunction= compareStations)
    return analyzer
    
# ==============================
# Funciones para agregar informacion al grafo
# ==============================

def addLine(analyzer, line):
    updateDateIndex(analyzer['DateIndex'], line)
    updateGraph(analyzer,line)
    return analyzer       

#----------------------------
# Requerimiento 2
#----------------------------
def updateDateIndex(map, line):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona al árbol.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea.
    """
    occurreddate = line['trip_start_timestamp']
    linedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%dT%H:%M:%S.%f')
    entry = om.get(map, linedate.date())
    if entry is None:
        datentry = {}
        om.put(map, linedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    calculatePoints(datentry,line)
    #addDateIndex(datentry, line, pointdic)
    return map
#----------------------------
# Requerimiento 3
#----------------------------    

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
#----------------------------
# Requerimiento 2
#----------------------------
    
def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['DateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['DateIndex'])

def getBestNTaxisByDate(analyzer, Date, N):
    """
    Para una fecha determinada, retorna el mejores N taxis.
    """
    qeue=pq.newMinPQ(cmpfunction= compareDegreeMax)
    Date = om.get(analyzer['DateIndex'], Date)
    try:
        if Date['key'] is not None:
            entry = me.getValue(Date)
            for taxi in entry:
                points=entry[taxi]["points"]
                pq.insert(qeue,{"id":taxi,"points":points})
            return qeue
    except:
        return 0

def getBestMTaxisByRange(analyzer,initDate, finalDate, M):
    dateslist=om.keys(analyzer['DateIndex'],initDate,finalDate)
    if lt.isEmpty(dateslist):
        return 0
    iterator=it.newIterator(dateslist)
    pointdic={}
    while it.hasNext(iterator):
        date=it.next(iterator)
        dictaxis=me.getValue(om.get(analyzer["DateIndex"],date))
        for tid in dictaxis:
            if tid not in pointdic:
                pointdic[tid]={"miles":0,"total":0,
                        "services":0,"points":0}
            pointdic[tid]["miles"]+=dictaxis[tid]["miles"]
            pointdic[tid]["total"]+=dictaxis[tid]["total"]
            pointdic[tid]["services"]+=dictaxis[tid]["services"]
            if pointdic[tid]["total"]!=0:
                pointdic[tid]["points"]=pointdic[tid]["miles"]*pointdic[tid]["services"]/pointdic[tid]["total"]
    qeue=pq.newMinPQ(cmpfunction= compareDegreeMax)
    for taxi in pointdic:
        points=pointdic[taxi]["points"]
        pq.insert(qeue,{"id":taxi,"points":points})
    return qeue
#----------------------------
# Requerimiento 3
#----------------------------

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

def calculatePoints(datentry,line):
    tid=line["taxi_id"]
    dic=datentry
    if tid not in dic:
        dic[tid]={"miles":0,"total":0,
                                    "services":0,"points":0}
    try:
        dic[tid]["miles"]+=float(line["trip_miles"])
        dic[tid]["total"]+=float(line["trip_total"])
        dic[tid]["services"]+=1
    except:
        pass
    if dic[tid]["total"]!=0:
        dic[tid]["points"]=dic[tid]["miles"]*dic[tid]["services"]/dic[tid]["total"]
    return None

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
def compareIds(id1, id2):
    
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
        
def compareStations(stop, keyvaluestop):
    
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareDegreeMax(value1,value2):
    value1 = value1["points"]
    value2 = value2["points"]
    if value1 == value2:
        return 0
    elif value1 > value2:
        return -1
    else:
        return 1 