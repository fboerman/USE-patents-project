__author__ = 'williewonka'

from graphviz import Graph

G = Graph('TestCase', 'testcase.gz', 'circle')
G.AddNode('1','2')
G.AddNode('3','2')
G.AddNode('2','4')
G.AddNode('2','5')
G.AddNode('5','4')
G.AddNode('4','6')
G.AddNode('4','7')
G.AddNode('4','8')
G.AddNode('8','2')
G.SPLC()
G.Parse()