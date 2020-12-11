"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 *
 * Contribución de:
 * Darío Correal
 """

import config
assert config

"""
Este código está basado en las implementaciones propuestas en:
- Algorithms, 4th Edition.  R. Sedgewick
- Data Structures and Algorithms in Java, 6th Edition.  Michael Goodrich
"""


def newEdge2(va, vb, weight=0):
    """
    Crea un nuevo arco entrelos vertices va y vb
    """
    edge = {'vertexA': va,
            'vertexB': vb,
            'weight': weight,
            }
    return edge

def newEdge(va,vb):
    edge = {"vertexA": va,
            "vertexB": vb,
            "weight":  {}}
    return edge

def weight(edge):
    """
    Retorna el peso de un arco
    """
    return edge['weight']


def either(edge):
    """
    Retorna el vertice A del arco
    """
    return edge['vertexA']


def other(edge, vertex):
    """
    Retorna el vertice B del arco
    """
    return edge['vertexB']


def compareedges(edge1, edge2):
    """
    Compara dos arcos y retorna True si son iguales
    """
    e1v = either(edge1)
    e2v = either(edge2)

    if e1v == e2v:
        if other(edge1, e1v) == other(edge2, e2v):
            return True
    return False

def updateAverageWeight(graph, edge, newweight,time):
    """
    Actualiza el peso del arco entre los vertices usando el promedio entre los pesos
    """
    if time not in edge["weight"]:
        edge["weight"][time] = {"weight": int(newweight),
                                "count": 1,
                                "sum": int(newweight)}
    else:
        edge["weight"][time]["count"]+= 1
        edge["weight"][time]["sum"] += int(newweight)
        edge["weight"][time]["weight"] = edge["weight"][time]["sum"]/edge["weight"][time]["count"]