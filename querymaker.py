__author__ = 'williewonka'

import json
from splinter import Browser
import argparse
import sys
import openpyxl

parser = argparse.ArgumentParser(description='queries a give list of patents from json object')
parser.add_argument('--janus', dest='janus', action='store_true', help='activates logging in from janus')
parser.set_defaults(janus = False)
parser.add_argument('--username', nargs='?', const=1, type=str, default='', help='username for janus proxy service')
parser.add_argument('--password', nargs='?', const=1, type=str, default='', help='password for janus proxy service')
parser.add_argument('--driver', nargs='?', const=1, type=str, default='firefox', help='browser drive: chrome/firefox. default firefox')
parser.add_argument('--downloadtype', nargs='?', const=1, type=str, default='patents', help='datatype of download: patents/citations')

JANUS, USERNAME, PASSWORD, DRIVER, DOWNLOADTYPE  = parser.parse_args().janus, parser.parse_args().username, parser.parse_args().password, \
                                                   parser.parse_args().driver, parser.parse_args().downloadtype
if DOWNLOADTYPE == 'patents':
    #get the data info
    inputdata = json.loads(open("data.json", 'r').readlines()[0])
elif DOWNLOADTYPE == 'citations':
    sheet = openpyxl.load_workbook('patentdata.xlsx').get_active_sheet()
    inputdata = []
    for cell in sheet.columns[4]:
        inputdata.append(str(cell.value))
    inputdata.pop(0)
else:
    sys.exit('wrong downloadtype argument')

results = {}#dictioanry that holds the numer of found patents per company
#create a browser bot and visit the website
try:
    browser = Browser(DRIVER)
except:
    sys.exit('failed to load specified driver ' + DRIVER)

#go to the database
if JANUS:
    url = 'http://apps.webofknowledge.com.dianus.libr.tue.nl/DIIDW_AdvancedSearch_input.do?' \
          'SID=V2i7L6wGDEBBsnkAWFI&product=DIIDW&search_mode=AdvancedSearch'
    browser.visit(url)
    #this redirects to janus, fill in login info
    browser.fill('user',USERNAME)
    browser.fill('pass', PASSWORD)
    #find and click the login button
    browser.find_by_value('Login').first.click()
    #if new session needs to be started click link
    try:
        browser.find_link_by_partial_text('new session').first.click()
    except:
        pass
else:
    url = 'http://apps.webofknowledge.com/DIIDW_AdvancedSearch_input.do?SID=N1cpglrQOdCmC16gM44&product=DIIDW&search_mode=AdvancedSearch'
    browser.visit(url)

def Build_Query_Citations(codes):
    #iterate through the list
    #build the query
    query = "CD=("
    for code in codes:
        if query == "CD=(":
            query += code
        else:
            query += " OR " + code
    query += ")"

    return query

def Build_Query_Patents(patents):
    #iterate through the patents
    #build the query
    query = "PN=("
    for patent in patents:
        if query == "PN=(":
            query += patent
        else:
            query += " OR " + patent
    query += ")"

    return query

def Execute_Query(patents,company,query):
    if browser.url != url:
        browser.visit(url)
    #fil it in the query and click serch
    browser.fill('value(input1)', query)
    browser.find_by_css('.searchButtons').first.click()
    #open the searchresults
    try:
        resultlink = browser.find_link_by_partial_href('summary.do').first
        if company != "":
            try:
                results[company]['resultsize'] += int(resultlink.value)
            except:
                results[company]['resultsize'] = int(resultlink.value)
        resultlink.click()
        #look for number of pages in result
        pages = int(browser.find_by_id('pageCount.top').value)
        for i in range(1,pages+1):
            #select all patents
            browser.find_by_name('SelectPage').first.click()
            #add everything to marked list
            browser.find_by_css(".addToMarkedList").first.click()
            #click on the next page button
            try:
                browser.find_by_css('.paginationNext').first.click()
            except:
                pass
        print("queried " + str(len(patents)) + " patents for company " + company)
    except KeyboardInterrupt:
        print('no patents found for ' + company)

def chunks(l, n):
    #Yield successive n-sized chunks from l.
    for i in range(0, len(l), n):
        yield l[i:i+n]

input()
if DOWNLOADTYPE == 'patents':
    for company in list(inputdata.keys()):
        patents = inputdata[company]
        results[company] = {
            'querysize' : len(patents)
        }
        for list_of_patents in chunks(patents,50):
            Execute_Query(list_of_patents,company,Build_Query_Patents(list_of_patents))

    print("parsing and saving results")
    JSON = json.dumps(results)
    stream = open('results.json', 'w')
    stream.writelines(JSON)
    stream.close()
    print('results saved')
elif DOWNLOADTYPE ==  'citations':
    for list_of_codes in chunks(inputdata,50):
        Execute_Query(list_of_codes,"",Build_Query_Citations(list_of_codes))
