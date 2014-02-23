__author__ = 'williewonka'

import json
from splinter import Browser
import argparse

parser = argparse.ArgumentParser(description='queries a give list of patents from json object')
parser.add_argument('--janus', dest='janus', action='store_true', help='activates logging in from janus')
parser.set_defaults(janus = False)
parser.add_argument('--username', nargs='?', const=1, type=str, default='', help='username for janus proxy service')
parser.add_argument('--password', nargs='?', const=1, type=str, default='', help='password for janus proxy service')

JANUS, USERNAME, PASSWORD = parser.parse_args().janus, parser.parse_args().username, parser.parse_args().password
#get the json info
inputjson = json.loads(open("data.json").readlines()[0])

#create a browser bot and visit the website

browser = Browser('firefox')

#go to the database
if JANUS:
    browser.visit('http://apps.webofknowledge.com.dianus.libr.tue.nl/DIIDW_AdvancedSearch_input.do?'
              'SID=V2i7L6wGDEBBsnkAWFI&product=DIIDW&search_mode=AdvancedSearch')
else:
    browser.visit('http://apps.webofknowledge.com/')

#this redirects to janus, fill in login info
browser.fill('user',USERNAME)
browser.fill('pass', PASSWORD)
#find and click the login button
browser.find_by_value('Login').first.click()

#redirects to the derwin sit
patentlist = {
    'Hitachi Maxell, Ltd.3' : inputjson['Hitachi Maxell, Ltd.3'],
    'Robert Bosch GmbH' : inputjson['Robert Bosch GmbH']
}

for company in list(patentlist.keys()):
    patents = [company]
    #iterate through the patent
    #build the query
    query = "PN=("
    for patent in patents:
        if query == "PN=(":
            query += patent
        else:
            query += " OR " + patent
    query += ")"
    #fil it in and click search
    browser.fill('value(input1)', query)
    browser.find_by_css('.searchButtons').first.click()
    #open the searchresults
    browser.click_link_by_partial_href('summary.do')
    #select all patents
    browser.find_by_name('SelectPage').first.click()
    #add everything to marked list
    browser.find_by_css(".addToMarkedList").first.click()

    #go back and fill in next query
    browser.visit('http://apps.webofknowledge.com.dianus.libr.tue.nl/DIIDW_AdvancedSearch_input.do?'
                  'SID=V2i7L6wGDEBBsnkAWFI&product=DIIDW&search_mode=AdvancedSearch')

    print("queried " + str(len(patents)) + " patents for company " + company)
    input()

# browser.click_link_by_partial_href('AdvancedSearch').first.click()
# browser.fill('value(input1)', 'TEST FOO BAR')