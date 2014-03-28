__author__ = 'williewonka'

from time import strftime
from json import dumps

class Graph():
    def __init__(self, graphname, filename, shape):
        self.filename = filename
        self.shape = shape
        self.nodes = {}
        self.iterations = 0

    def StartFile(self):
        self.stream = open(self.filename, 'w')
        self.stream.write("digraph Test {\n\tnode [shape = " + self.shape + "];\n\tsplines=false;\n")

    def AddNode(self, parent, child):
        if parent in list(self.nodes.keys()):
            if child in list(self.nodes[parent].keys()):
                self.nodes[parent][child] += 1
            else:
                self.nodes[parent][child] = 1
        else:
            self.nodes[parent] = {
                child : 1
            }

    def AddNodeDirect(self, parent, child, color, label, noselfie=True):
        if parent == child and noselfie:
            return
        self.stream.write('\t' + parent + ' -> ' + child +  ' [label = ' + label + ', color = ' + color + '];\n')

    def Parse(self,categories=[5,10,20,50],filter=-1,factor=1):
        self.StartFile()
        for node in list(self.Edges.keys()):
            parent = node.split('.')[0]
            child = node.split('.')[1]
            count = round((self.Edges[node])/factor)
            if count <= filter:
                continue
            if count < categories[0]:
                color = 'black'
                penwidth = 1
                # continue
            elif categories[0] <= count <= categories[1]:
                color = 'blue'
                penwidth = 2
            elif categories[1] < count <= categories[2]:
                color = 'magenta'
                penwidth = 3
            elif categories[2] < count <= categories[3]:
                color = 'orange'
                penwidth = 4
            elif count > categories[3]:
                color = 'red'
                penwidth = 5
            self.stream.write('\t' + parent + ' -> ' + child +  ' [label="' + str(count) + '", color = ' + color + ','
                            ' penwidth = ' + str(penwidth) + '];\n')
        self.Close()

    def CreateEdgeList(self, Type):
        self.Edges = {}
        for parent in list(self.nodes.keys()):
            for child in list(self.nodes[parent].keys()):
                if Type == 'citations':
                    self.Edges[parent + '.' + child] = self.nodes[parent][child]
                elif Type == 'SPLC':
                    self.Edges[parent + '.' + child] = 0
        return self.Edges

    def Close(self):
        self.stream.write('}')
        self.stream.close()

    def AllChildren(self):
        List = []
        for childrenlist in list(self.nodes.values()):
            for children in childrenlist:
                if children not in List:
                    List.append(children)
        List.sort()
        return List

    def AllParents(self):
        List = list(self.nodes.keys())
        List.sort()
        return List

    def FindBeginPoints(self):
        BeginPoints = []
        AllChildren = self.AllChildren()
        for parent in self.AllParents():
            if parent not in AllChildren:
                BeginPoints.append(int(parent))
        BeginPoints.sort()
        return BeginPoints


    def FindEndPoints(self):
        EndPoints = []
        AllParents = self.AllParents()
        for child in self.AllChildren():
            if child not in AllParents:
                EndPoints.append(int(child))
        EndPoints.sort()
        return EndPoints

    def WalkNext(self, parent, child, visitededges, visitednodes):
        #DEBUG
        # if self.iterations > 1000000:
        #     self.DebugDump('infinite loop SPLC',[visitednodes,visitededges])
        self.iterations += 1
        # print(parent + '.' + child)
        # self.debug.write(parent + '.' + child + "\n")

        #FUNCTION
        visitededges.append(parent + '.' + child)
        visitednodes.append(child)
        if int(child) in self.FindEndPoints():
            for edge in visitededges:
                self.Edges[edge] += 1
            visitededges.pop()
            visitednodes.pop()
            return
        for c in list(self.nodes[child].keys()):
            if child + '.' + c in visitededges or c in visitednodes:
                continue
            self.WalkNext(child,c,visitededges,visitednodes)
        visitededges.pop()
        visitednodes.pop()

    def SPLC(self, dump=False):
        # self.debug = open('debug.txt','w')
        self.CreateEdgeList('SPLC')
        for beginpoint in self.FindBeginPoints():
            for child in list(self.nodes[str(beginpoint)].keys()):
                print('Finished ' + str(beginpoint) + '.' + str(child) + ' in ' + str(self.iterations) + ' iterations at ' + strftime("%H:%M:%S"))
                self.iterations = 0
                self.WalkNext(str(beginpoint), str(child),[],[beginpoint])
        # self.debug.close()
        # self.DebugDump('done',[])
        if dump:
            stream = open("json/outputedges.json", "w")
            stream.writelines(dumps(self.Edges))
            stream.close()

    def Dump(self):
        stream = open('json/edges.json', 'w')
        stream.writelines(dumps(self.Edges))
        stream.close()
        fixed_nodes = {}
        for node in list(self.nodes.keys()):
            for child in list(self.nodes[node]):
                try:
                    fixed_nodes[node].append(int(child))
                except:
                    fixed_nodes[node] = []
                    fixed_nodes[node].append(int(child))
        stream = open('json/nodes.json', 'w')
        stream.writelines(dumps(fixed_nodes))
        stream.close()
        stream = open('json/beginpoints.json', 'w')
        stream.writelines(dumps(self.FindBeginPoints()))
        stream.close()
        stream = open('json/endpoints.json', 'w')
        stream.write(dumps(self.FindEndPoints()))
        stream.close()

#    def DebugDump(self,error,dumplist):
#        self.debug.close()
#        stream = open('debug.json','w')
#        stream.writelines(dumps(self.Edges)+'\n'+dumps(self.nodes)+'\n')
#        for dump in dumplist:
#            stream.writelines(dumps(dump)+'\n')
#       stream.close()
#        self.debug.close()
#        self.Parse()
#        raise Exception(error)