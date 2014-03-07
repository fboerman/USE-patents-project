__author__ = 'williewonka'
from json import loads
import openpyxl
from decimal import Decimal

#compile big list of all found patent numbers
wb = openpyxl.load_workbook('patentdata_run2.xlsx')
sheet = wb.get_active_sheet()

patentlistfound = []
patentnumbers = sheet.columns[0]
for cell in patentnumbers:
    for patent in cell.value.split(';'):
        patentlistfound.append(patent.split('-')[0].strip())


notfound = 0
total = 0

inputjson = loads(open('data_valid.json','r').readlines()[0])
stream = open('notfound.txt','w')
for company in list(inputjson.keys()):
    patents = inputjson[company]
    for patent in patents:
        total += 1
        if patent not in patentlistfound:
            line = "patent " + patent + " from " + company + " not found!"
            print(line)
            stream.write(line + '\n')
            notfound += 1

percentage = (notfound/total)*100
line = '\ntotal not found: ' + str(notfound) + " from total of " + str(total) + " misratio of " + str(Decimal(str(percentage)).quantize(Decimal('.01'))) + '%'
print(line)
stream.write(line)
stream.close()