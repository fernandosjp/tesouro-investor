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
#import email #import sendMail
# Logging
import logging
#Others
import datetime

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


def convertToInt(x):
	"""
	Function to convert yield to integer
	"""
	try:
		x=float(x)/10000
	except Exception, e:
		x=0
	return x

def saveTask(emailSent):
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


to = ['REMOVED',
	  'REMOVED'
]
msgText = ""
subject = "[Tesouro Direto] Alerta COMPRA TUDO - LTN >= 16%"

df = dfList[0]
df.dropna(inplace=True)

logger.info('Correcting Bond Yields')
df['taxa'] = df.apply(lambda row: convertToInt(row['Compra.1']), axis=1)

msgText=df.to_html()

logger.info('Check condition')

emailSent = False

if not df.query("taxa>=0.16").empty:
	logger.info('Condition satisfied!!')
	try:
		logger.info('Sending Email...')
		print "emial sent"#sendMail.sendEmail(subject, msgText, to, sender = 'Tesouro Invest')
	except Exception, e:
		logger.info('Email not sent...')
	finally:
		emailSent = True
		logger.info('Email sent!')
else:
	logger.info('No bonds today!!')

logger.info('Saving task in DB...')
saveTask(emailSent)
