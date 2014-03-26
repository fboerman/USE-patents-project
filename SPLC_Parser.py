__author__ = 'williewonka'

from graphviz import Graph
from json import loads

G = Graph("SPLC", "SPLC_RESULT.dot", "circle")

G.Edges = loads(open("json/RESULT.json", "r").readlines()[0])

G.Parse(categories=[10,30,40,55],factor=1000000,filter=15)