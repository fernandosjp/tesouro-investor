#!/home/fernandosjp/anaconda/bin/python

# Bond Scrapper
from lxml.html import parse
from lxml import etree
from urllib2 import urlopen
from pandas.io.parsers import TextParser
# Data
import pandas as pd
# Logging
import logging
#Regexp 
import re

class BondScrapper(object):
	"""
	BondScrapper is responsible for accessing Tesouro Direto website and returning a DataFrame containing the following columns:

	1. Titulo
	2. Vencimento
	3. Taxa Compra
	4. Taxa Venda
	5. Preco Compra
	6. Preco Venda

	"""

	def __unpack(self, row, kind='td'):
		elts = row.findall('.//%s' % kind)
		return [val.text_content() for val in elts]

	def __parse_options_data(self, table):
		rows = table.findall('.//tr')
		#TODO: understand how to make header parser generic
		#header = __unpack(rows[0], kind='th')
		header = ['titulo','vencimento','taxa_compra','taxa_venda','preco_compra','preco_venda']
		data = [self.__unpack(r) for r in rows[2:]]
		return TextParser(data, names=header).get_chunk()

	def __convertToInt(self, x):
		"""
		Function to convert yield to integer
		"""
		try:
			x=float(x)/10000
		except Exception, e:
			x=0
		return x

	def __extractBondName(self, x):
	    searchString = re.search(r"\(([^)]+)\)", str(x))
	    bondName=""
	    try:
	        bondName = searchString.group(1)
	    except:
	        pass
	    
	    return bondName

	def getBondTable(self):
		"""
		Opens url and returns bond table in a Data Frame with the columns [titulo,vencimento,taxas]
		-----

		Return Data Frame
		
		"""
		#Open a browser
		url='http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos'
		#logger.info('Opening url: {}'.format(url))
		parsed = parse(urlopen('http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos'))
		doc = parsed.getroot()
		tables = doc.findall('.//table')

		df = self.__parse_options_data(tables[1])
		df.dropna(inplace=True)

		#logger.info('Correcting Bond Yields')
		df['taxa'] = df.apply(lambda row: self.__convertToInt(row['taxa_compra']), axis=1)
		df['titulo'] = df.apply(lambda row: self.__extractBondName(row['titulo']), axis=1)
		
		columns = ['titulo','vencimento','taxa_compra']

		return df[columns]




