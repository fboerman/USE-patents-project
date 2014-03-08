__author__ = 'williewonka'

class Graph():
    def __init__(self, graphname, filename, shape):
        self.filename = filename
        self.shape = shape
        self.nodes = {}

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

    def AddNodeDirect(self, parent, child, color, label):
        self.stream.write('\t' + parent + ' -> ' + child +  ' [label = ' + label + ', color = ' + color + '];\n')

    def Parse(self,categories=[5,10,20,50]):
        self.StartFile()
        for node in list(self.Edges.keys()):
            parent = node.split('.')[0]
            child = node.split('.')[1]
            count = self.Edges[node]
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
                    self.Edges[parent + '.' + child] = 1
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

    def WalkNext(self, parent, child, alreadydone):
        print(parent + '.' + child)
        self.debug.write(parent + '.' + child + "\n")
        self.Edges[parent + '.' + child] += 1
        if int(child) in self.FindEndPoints():
            return
        for c in list(self.nodes[child].keys()):
            # if int(c) in self.FindEndPoints():
            #     self.Edges[child + '.' + c] += 1
            if c in alreadydone:
                continue
            if c not in self.FindEndPoints():
                alreadydone.append(c)
                self.WalkNext(child,c,alreadydone)
            else:
                self.WalkNext(child,c,alreadydone)

    def SPLC(self):
        self.debug = open('debug.txt','w')
        self.CreateEdgeList('SPLC')
        for beginpoint in self.FindBeginPoints():
            for child in list(self.nodes[str(beginpoint)].keys()):
                self.WalkNext(str(beginpoint),child,[str(beginpoint),child])
        self.debug.close()