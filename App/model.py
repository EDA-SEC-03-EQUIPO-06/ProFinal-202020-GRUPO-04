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
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import quicksort as qs
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
                "DateIndex": None,
                "graph": None}
    analyzer["CompanyServices"] = m.newMap(comparefunction=)
    analyzer["CompanyTaxis"] = m.newMap(comparefunction=)

    analyzer['Services'] = lt.newList('ARRAY_LIST', compareIds)
    analyzer["DateIndex"] = om.newMap(omaptype= "RBT",
                                      comparefunction=compareDates)
    analyzer["graph"] = gr.newGraph(datastructure= "ADJ_LIST",
                                    directed = True,
                                    comparefunction=)
    return analyzer
    
# ==============================
# Funciones para agregar informacion al grafo
# ==============================

def addLine(analyzer, line):
    #company = tripfile[""]
    lt.addLast(analyzer["Services"],line)
    updateDateIndex(analyzer['DateIndex'], line)
    return analyzer       

#----------------------------
# Requerimiento 2
#----------------------------
def updateDateIndex(map, line, pointdic):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona al árbol.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea.
    """
    occurreddate = line['trip_start_timestamp']
    linedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, linedate.date())
    if entry is None:
        datentry = {}
        om.put(map, linedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    calculatePoints(datentry,line)
    #addDateIndex(datentry, line, pointdic)
    return map

# ==============================
# Funciones de consulta
# ==============================
#----------------------------
# Requerimiento 2
#----------------------------
def TaxisSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['Services'])
    
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
    i=0
    lista=[]
    try:
        if Date['key'] is not None:
            entry = me.getValue(Date)
            for taxi in entry:
                points=entry[taxi]["points"]
                pq.insert(qeue,{"id":taxi,"points":points})
            while i<N:
                lista.append(pq.delMin(qeue))
                i+=1
            return lista
    except:
        return 0

def getBestMTaxisByRange(analyzer,i nitDate, finalDate, M):
    Mapas=om.values(analyzer['DateIndex'],initDate,finalDate)
    print(Mapas)

# ==============================
# Funciones Helper
# ==============================

#----------------------------
# Requerimiento 2
#----------------------------
def calculatePoints(datentry,line):
    tid=line["taxi_id"]
    dic=datentry
    #dic=datentry["PointDic"]
    if tid not in dic:
        dic[tid]={"miles":0,"total":0,
                                    "services":0,"points":0}
    dic[tid]["miles"]+=line["trip_miles"]
    dic[tid]["total"]+=line["trip_total"]
    dic[tid]["services"]+=1
    dic[tid]["points"]=dic[tid]["miles"]*dic[tid]["services"]/dic[tid]["total"]
    return None


# ==============================
# Funciones de Comparacion
# ==============================

#----------------------------
# Requerimiento 2
#----------------------------
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
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






"""
def newDataEntry(line):
  
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    
    entry = {"PQ":None, "listTaxis":None, "PointDic"={}}
    entry['PQ'] = pq.newMinPQ(cmpfunction= compareDegreeMax)
    entry["listTaxis"]=lt.newList('ARRAY_LIST', compareIds)
    return entry

def addDateIndex(datentry, line, pointdic):
    pq=datentry["PQ"]
    listTaxis=datentry["listTaxis"]
    tid=line["taxi_id"]
    points=pointdic["tid"]["points"]
    if not lt.isPresent(listTaxis,tid):
        lt.addLast(listTaxis,tid)
        pq.insert(pq,{tid:points})
    return datentry

def addtoTree(analyzer)
    i=it.newIterator(analyzer["Services"])
    while it.hasNext(i):
        line=it.next(i)
        updateDateIndex(analyzer['DateIndex'], line , analyzer["PointDic"])
    return None
"""