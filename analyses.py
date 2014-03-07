__author__ = 'williewonka'

from textmining import TextMining

analyzer = TextMining('patentdata.xlsx')

analyzer.Parse_Categories('categorien.xlsx')