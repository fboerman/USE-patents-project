__author__ = 'Williewonka'

import openpyxl

class TextMining:

    def __init__(self, mainFileName, ExportName, rawinput):
        self.mainFileName = mainFileName
        self.ExportName = ExportName
        self.rawinput = rawinput
        self.droplist = ["", "the", "a", "an", "on", "can", "is", "not", "and", "are", "to", "in", "for", "as", "of", "it", "if", "in", "e.g", "i.e",
                         "or", "at","by", "be", "so", "with", "thus", "with", "use", "from", "such", "has", "into", "over", "via", "which", "but",
                         "that"]
        self.wb = openpyxl.load_workbook(self.mainFileName)
        self.sheet = self.wb.get_active_sheet()
        
    def Parse_Company_Counting(self):
        companies = {}
        data = (self.sheet.columns[0], self.sheet.columns[3])
        for i in range(0, len(data[0])):
            for entry in data[1][i].value.split(";"):
                entry = entry.strip()
                company = ""
                company = entry.split("(")[1].split(")")[0].split("-")[0]
                try:
                    countrylist = companies[company]
                except:
                    countrylist = {}
                for code in data[0][i].value.split(";"):
                    code = code.strip()
                    countrycode = code[0] + code[1]
                    try:
                        countrylist[countrycode] += 1
                    except:
                        countrylist[countrycode] = 1
                companies[company] = countrylist
        exportwb = openpyxl.Workbook()
        sheet = exportwb.get_active_sheet()
        columns = []

        for countrylist in list(companies.values()):
            for country in list(countrylist.keys()):
                if country not in columns:
                    columns.append(country)

        columns = sorted(columns)
        for i in range(0,len(columns)):
            sheet.cell(row=0,column=(i+1)).value = columns[i]

        for i in range(0, len(list(companies.keys()))):
            sheet.cell(row=(i+1),column=0).value = list(companies.keys())[i]
            for country in list(list(companies.values())[i].keys()):
                sheet.cell(row=(i+1),column=(columns.index(country) + 1)).value = list(companies.values())[i][country]
        exportwb.save(self.ExportName)

    def Parse_Word_Counting(self):
        data = self.sheet.columns[1]
        categories = {}
        for row in data:
            #splitten naar de aparte categoriën
            #verwijder de eerste lege entry
            try:
                parts = row.value.split("   ")
            except:
                continue
            parts.pop(0)
            for part in parts:
                #extract de naam van categorie
                categorie = part.split(" - ")[0].strip()
                if len(part.split(" - ")) < 2:
                    continue
                text = part.split(" - ")[1].strip()
                #kijk of categorie al bestaat, indien niet creeër
                try:
                    categorielist = categories[categorie]
                except:
                    categories[categorie] = {}
                    categorielist = {}
                #splits op spaties voor alle woorden
                for woord in text.split(" "):
                    #kijk of woord al in lijst staat
                    woord = woord.lower().strip(".").strip(",").strip(";")
                    #kijk of het een getal is
                    try:
                        float(woord)
                        continue
                    except:
                        pass
                    if woord not in self.droplist and "(" not in woord and ")" not in woord: #controleer tegen de filteropties
                        try:
                            categorielist[woord] += 1
                        except:
                            categorielist[woord] = 1
                    else:
                        continue
                categories[categorie] = categorielist

            print("row: " + row.address.split("F")[1])

        #exporteer de data
        exportwb = openpyxl.Workbook()
        for categorie in list(categories.keys()):
            exportwb.create_sheet(title=categorie)
            sheet = exportwb.get_sheet_by_name(categorie)
            for i in range(0,len(categories[categorie])):
                sheet.cell(row=i, column=0).value = list(categories[categorie].keys())[i]
                sheet.cell(row=i, column=1).value = list(categories[categorie].values())[i]
                
        #verwijder de standaard aangemaakte sheet:
        sheet = exportwb.get_sheet_by_name("Sheet")
        exportwb.remove_sheet(sheet)
        exportwb.save(self.ExportName)

    def Parse_Categories(self, ExportName):
        data = self.sheet.columns[5]
        categories = {}
        for row in data:
            for entry in row.value.split(";"):
                entry = entry.strip()
                try:
                    categorie = entry.split("(")[1].split(")")[0]
                except:
                    continue
                try:
                    categories[categorie] += 1
                except:
                    categories[categorie] = 1

        #export the data
        exportwb = openpyxl.Workbook()
        exportsheet = exportwb.get_active_sheet()
        for i in range(0, len(categories)):
            exportsheet.cell(row=i,column=0).value = list(categories.keys())[i]
            exportsheet.cell(row=i,column=1).value = list(categories.values())[i]
        exportwb.save(ExportName)