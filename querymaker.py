__author__ = 'williewonka'
__username__ = ''
__password__ = ''

import json
from splinter import Browser

#get the json info
inputjson = json.loads(open("data.json").readlines()[0])

#create a browser bot and visit the website

browser = Browser('firefox')

#go to the database
browser.visit('http://apps.webofknowledge.com.dianus.libr.tue.nl/DIIDW_AdvancedSearch_input.do?SID=V2i7L6wGDEBBsnkAWFI&product=DIIDW&search_mode=AdvancedSearch')
#this redirects to janus, fill in login info
browser.fill('user', __username__)
browser.fill('pass', __password__)
#find and click the login button
browser.find_by_value('Login').first.click()

#redirects to the derwin site, build the query and fill it in
query = "PN=("
for patent in list(inputjson.values())[0]:
    if query == "PN=(":
        query += patent
    else:
        query += " OR " + patent
query += ")"
browser.fill('value(input1)', query)
browser.find_by_css('.searchButtons').first.click()