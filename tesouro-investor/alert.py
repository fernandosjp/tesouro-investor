#!/home/fernandosjp/anaconda/bin/python

# Crawler
import mechanize
from BeautifulSoup import BeautifulSoup
# Visualization
from IPython.display import display, HTML
# Data
import pandas as pd
import sqlite3
# Emails
from emailSender import *
# Logging
import logging
#Others
import datetime
#Regexp 
import re 
import json

#Logging
# create logger with 'alert tesouro'
logger = logging.getLogger('alert_tesouro')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('alertInvest.log')
fh.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
eh = logging.FileHandler('alertInvestError.log')
eh.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
eh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(eh)

class Alert(object):
	"""

	"""
	def __init__(self, alerts):
		"""
		import alerts
		"""
		with open('alerts.json') as json_data_file:
		    self.alerts = json.load(json_data_file)

	def convertToInt(self, x):
		"""
		Function to convert yield to integer
		"""
		try:
			x=float(x)/10000
		except Exception, e:
			x=0
		return x

	def extractBondName(self, x):
	    searchString = re.search(r"\(([^)]+)\)", str(x))
	    bondName=""
	    try:
	        bondName = searchString.group(1)
	    except:
	        pass
	    
	    return bondName

	def saveTask(self, emailSent):
		# Connecting to the database file
		sqlite_file = 'alertInvest.sqlite'  
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		try:
			c.execute("INSERT INTO job_logs (date_task, emailSent) VALUES (?,?)", (now,emailSent))
			logger.info('Successfully inserted in database!')
		except Exception, e:
			logger.error('Not able to INSERT in database!')

		conn.commit()
		conn.close()

		return None

	def getBondTable(self):
		"""
		Opens url and returns bond table in a Data Frame with the columns [titulo,vencimento,taxas]
		-----

		Return Data Frame
		
		"""
		#Open a browser
		logger.info('Opening browser')
		br = mechanize.Browser()
		br.addheaders = [('User-agent', 'Firefox')]
		br.set_handle_robots(False)

		#Open a url
		url='http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos'
		logger.info('Opening url: {}'.format(url))
		page = br.open(url)

		logger.info('Reading url: {}'.format(url))
		html = page.read()
		soup = BeautifulSoup(html)

		logger.info('Getting tables from html')
		tables = soup.findAll("table")

		logger.info('Importing html tables to Pandas')
		dfList = pd.read_html(str(tables[1]), header=True)

		df = dfList[0]
		df.dropna(inplace=True)
		print df
		logger.info('Correcting Bond Yields')
		df['taxa'] = df.apply(lambda row: self.convertToInt(row['Compra.1']), axis=1)
		df['titulo'] = df.apply(lambda row: self.extractBondName(row['Compra']), axis=1)

		rename = {'Venda':'vencimento'}
		df.rename(columns=rename, inplace=True)
		
		columns = ['titulo','vencimento','taxa']

		return df[columns]

	def sendEmailAlert(self, df):

		to = ['REMOVED',
			  #'REMOVED'
		]
		msgText = ""
		subject = "[Tesouro Direto] Alerta COMPRA TUDO - LTN >= 16%"
		msgText=df.to_html()

		sendMail.sendEmail(subject, msgText, to, sender = 'Tesouro Invest')

		return None

	def alert_trigger(self, alert):
		
		logger.info('Check condition')
		
		emailSent = False
		
		#TODO: taxas vindo zeradas
		if not self.bonds_table.query("taxa>=0.14").empty:
			logger.info('Condition satisfied!!')
			try:
				logger.info('Sending Email...')
				sendEmailAlert(df)	
			except Exception, e:
				logger.info('Email not sent...')
			finally:
				emailSent = True
				logger.info('Email sent!')
		else:
			logger.info('No bonds today!!')

		logger.info('Saving task in DB...')
		self.saveTask(emailSent)

		return None

	def run(self):

		self.bonds_table = self.getBondTable()

		for alert in self.alerts:
			self.alert_trigger(alert)

if __name__ == "__main__":

	alert = Alert('alerts.json')
	alert.run()
	


