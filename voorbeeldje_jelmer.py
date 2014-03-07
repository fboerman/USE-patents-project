__author__ = 'williewonka'

import json

dictionary = json.loads(open('data.json','r').readlines()[0])

for bedrijf in list(dictionary.keys()):
    print('patenten van: ' + bedrijf)
    for patent in dictionary[bedrijf]:
        print(patent)