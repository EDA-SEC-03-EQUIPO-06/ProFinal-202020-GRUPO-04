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
from DISClib.ADT import minpq as pq
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    analyzer = {"Company": None,
                "Total_Taxis": [],
                "Total_Companys": None, 
                "DatesTree": None,
                "graph": None}
    
    analyzer["Company"] = m.newMap(comparefunction=compareMap)
    analyzer["Total_Companys"] = 0
    analyzer["DatesTree"] = om.newMap(omaptype= "RBT",
                                      comparefunction=compareMap)
    analyzer["graph"] = gr.newGraph(datastructure= "ADJ_LIST",
                                    directed = True,
                                    comparefunction=compareMap)
    return analyzer
    
# ==============================
# Funciones para agregar informacion al grafo
# ==============================

def addLine(analyzer, tripfile):
    addCompanyService(analyzer, tripfile)


def addCompanyService(analyzer, tripfile):
    mapa = analyzer["Company"]
    Compañia = tripfile["company"]
    taxiID = tripfile["taxi_id"]
    lsttaxis = analyzer["Total_Taxis"]
    
    if Compañia == None or Compañia == "" or Compañia == " ": 
        Compañia = "Independent Owner"
    
    existcompany = m.contains(mapa, Compañia)

    if existcompany:
        consulta = m.get(mapa, Compañia)['value']
        consulta["Services"] += 1
        if taxiID not in consulta["Taxis"]:
            consulta["Taxis"].append(taxiID)
            consulta["numTaxis"] +=1
        
        
    else:
        analyzer["Total_Companys"] += 1
        DictCompany = newCompany()
        m.put(mapa, Compañia, DictCompany)
        m.get(mapa, Compañia)['value']["Services"] += 1

    if taxiID not in lsttaxis: 
            lsttaxis.append(taxiID)

        

    

# ==============================
# Funciones de consulta
# ==============================
def Total(analyzer):

    return {"Total_Taxis: ": (len(analyzer["Total_Taxis"])), "Total_Companys: ": analyzer["Total_Companys"] }

def PQmaker(analyzer): 
    
    TopServices =  pq.newMinPQ(cmpfunction= comparefunction)
    TopTaxis = pq.newMinPQ(cmpfunction= comparefunction)
    lstcompany = m.keySet(analyzer["Company"])
    iterator = it.newIterator(lstcompany)}

    while it.hasNext(iterator):
        element = it.next(iterator)
        consulta = m.get(analyzer["Company"], element)['value']
        
        numtaxis = len(consulta["Taxis"])
        numservices = (consulta["Services"])
        print(numtaxis, numservices, element)

        taxisentry = {"key": numtaxis, "company": element}
        servicesentry = {"key": numservices, "company": element}
        
        pq.insert(TopTaxis, taxisentry)
        pq.insert(TopServices, servicesentry)

    return {"T_taxis": TopTaxis, "T_services": TopServices}




# ==============================
# Funciones Helper
# ==============================
def newCompany():
    r = {"Taxis": [],"numTaxis":0, "Services": 0}
    return r

def getTopN(Pq, n):
    Taxis = {}
    Services = {}
    
    for i in range(1, n+1):
        Taxis[i] = pq.delMin(Pq["T_taxis"])
        Services[i] = pq.delMin(Pq["T_services"])
    
    return (Taxis, Services) 

# ==============================
# Funciones de Comparacion
# ==============================
def compareMap(keyname,company):
    companyentry = me.getKey(company)
    if keyname==companyentry:
        return 0
    elif keyname > companyentry:
        return 1
    else:
        return -1

def comparefunction(value1,value2):
    value1 = value1["key"]
    value2 = value2["key"]
    if value1 == value2:
        return 0
    elif value1 < value2:
        return 1
    else:
        return -1