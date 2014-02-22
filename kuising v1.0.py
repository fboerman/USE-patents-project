__author__ = 'williewonka'

import json

file = open("data raw.txt", "r").readlines()
outputfile = open("data.txt", "w")
outputjson = open("data.json", "w")

data_net = []

companies = {}

#throw all page references out
for line in file:
    if "Page" in line and "February" in line:
        newline = line.split("February")[0] + "\n"
        data_net.append(newline)
        continue
    else:
        data_net.append(line)
        continue

#iterate through the file again and sort all patents per company in a dictionary that holds a list per company
i = 0
while i < len(data_net):
    line = data_net[i].strip('\n')
    if len(line.split(" ")[0]) > 2 and "AT-E" not in line:
        j = i + 1
        company = line
        companies[company] = []
        while j < len(data_net):
            line = data_net[j].strip('\n')
            if len(line.split(" ")[0]) > 2 and "AT-E" not in line:
                i = j - 1
                break
            companies[company].append(line)
            j += 1

    i += 1

#create json object and write to file
JSON = json.dumps(companies)
outputfile.writelines(data_net)
outputjson.writelines(JSON)