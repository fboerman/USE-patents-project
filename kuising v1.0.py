__author__ = 'williewonka'

from json import dumps

file = open("data raw.txt", "r").readlines()
outputfile = open("data.txt", "w")
# outputjson_valid = open("data_valid.json", "w")
# outputjson_expired = open("data_expired.json", "w")
outputjson = open('data.json', 'w')

data_net = []

# valid = {}
# expired = {}
patents = {}

#throw all page references out
for line in file:
    if "Page" in line and "February" in line:
        newline = line.split("February")[0] + "\n"
        data_net.append(newline)
        continue
    else:
        data_net.append(line)
        continue
#TODO:
#alleen US patents
#Re fixen

#iterate through the file again and sort all patents per company in a dictionary that holds a list per company
i = 0
while i < len(data_net):
    line = data_net[i].strip('\n')
    if len(line.split(" ")[0]) > 2 and "AT-E" not in line:
        j = i + 1
        company = line
        # valid[company] = []
        # expired[company] = []
        patents[company] = []
        while j < len(data_net):
            line = data_net[j].strip('\n')
            if len(line.split(" ")[0]) > 2 and "AT-E" not in line:
                i = j - 1
                break
            patent = line.split("-")[0].replace(' ', '').replace(',', '')
            if 'US' not in patent:
                j += 1
                continue
            if "Re" in patent:
                patent = patent.replace('Re.', '')
            patents[company].append(patent)
            # if 'Expired' in line:
            #     expired[company].append(patent)
            # else:
            #     valid[company].append(patent)
            j += 1

    i += 1

#create json object and write to file
# JSON_v = dumps(valid)
# JSON_e = dumps(expired)
JSON  = dumps(patents)
outputfile.writelines(data_net)
outputfile.close()
outputjson.writelines(JSON)
outputjson.close()
# outputjson_valid.writelines(JSON_v)
# outputjson_expired.writelines(JSON_e)
