__author__ = 'williewonka'
import openpyxl
from graphviz import Graph

#compile big list of all found patent numbers
wb = openpyxl.load_workbook('patentdata_run1.xlsx')
sheet = wb.get_active_sheet()

patentlisttotal = {}
patentnumbers = sheet.columns[0]
for cell in patentnumbers:
    for patent in cell.value.split(';'):
        row = int(''.join(x for x in cell.address if x.isdigit()))
        patentlisttotal[patent.split('-')[0].strip()] = row

data = (sheet.columns[0],sheet.columns[6])

G = Graph('Test','test2.gz','circle')
i = 0
for i in range(0,len(data[0])):
    citationlist = data[1][i].value
    if citationlist is None:
        continue
    # noinspection PyRedeclaration
    for citationentry in citationlist.split(";"):
        citationentry = citationentry.strip().split('   ')[0]
        for citation in citationentry.split(' -- '):
            if citation.split('-')[0] in list(patentlisttotal.keys()):
                # print('row ' + str(i) + ' cites row ' + str(patentlisttotal[citation.split('-')[0]]))
                G.AddNode(str(i), str(patentlisttotal[citation.split('-')[0]]))

# G.CreateEdgeList('citations')
G.SPLC()
G.Parse()
# EndPoints = G.FindEndPoints()
# BeginPoints = G.FindBeginPoints()
