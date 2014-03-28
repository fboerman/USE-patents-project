__author__ = 'williewonka'

from toolset_mapping import ToolBox
import openpyxl
from json import dumps
import sys

#globals
toolboxes = []
results = {} #dictionary of results, key is patent, value is dictionary with toolbox as key and weight as value
toolboxesresult = {} #dictionary of toolboxes, key is the number of toolbox, value is dictionary with key patent and value weight
#load the patentdata
wb = openpyxl.load_workbook("patentdata/patentdata.xlsx")
sheet = wb.get_active_sheet()
abstracts = sheet.columns[1]

#load the toolboxes encoding
stream = open("toolboxes.tb","r")
# toolboxfile = stream.readlines()
#create the seperate toolbox classes and store them in global
i = 0
for line in stream:
    line = line.strip("\n")
    # try:
    toolboxes.append(ToolBox(line))
    # except:
    #     sys.exit("Parse error at line " + str(i))
    i += 1


#iterate through the abstracts, remember the index number
i = 1 #skip first row
while i < len(abstracts):
    j = 0
    results[i] = {}
    while j < len(toolboxes):
        result = toolboxes[j].Check(abstracts[i].value.split(" "))
        if result == 0:
            j += 1
            continue
        try:
            toolboxesresult[j][i] = result
        except:
            toolboxesresult[j] = {}
            toolboxesresult[j][i] = result
        results[i][j] = result
        j += 1
    i += 1


#dump results
stream = open("json/toolboxresult_patents.json","w")
stream.writelines(dumps(results))
stream.close()
stream = open("json/toolboxresult_toolboxes.json","w")
stream.writelines(dumps(toolboxesresult))
stream.close()