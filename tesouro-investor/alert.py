#!/home/fernandosjp/anaconda/bin/python

# Visualization
from IPython.display import display, HTML
# Data
import pandas as pd
import sqlite3
# Emails
from emailSender.sendMail import Email
# Logging
import logging
#Others
import datetime
import json
import yaml
from  scrapper import BondScrapper

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
	Alert class is responsible for looping into predefined alerts and sending e-mails.
	"""
	def __init__(self, alerts):
		"""
		import alerts
		"""
		with open(alerts) as json_data_file:
		    self.alerts = json.load(json_data_file)

		# Load configuration
		with open('config.yml', 'r') as f:
			self.config = yaml.safe_load(f)

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

	def sendEmailAlert(self):

		email = Email(self.config['smtp'])
		msgText = ""
		subject = "[Tesouro Direto] Alerta COMPRA TUDO - {}".format(self.alertQuery)
		msgText=self.bonds_table.to_html()

		email.sendEmail(subject, msgText, sender = 'Tesouro Invest')

		return None

	def alert_trigger(self, alert):
		
		logger.info('Check condition: bond {BOND} and yield {YIELD}'.format(BOND = alert['bound_name'], YIELD = alert['yield']))
		
		self.alertQuery = "(taxa>={YIELD}) and (titulo=='{BOND}') ".format(YIELD = alert['yield'],
																		   BOND = alert['bound_name'])
		emailSent = False

		if not self.bonds_table.query(self.alertQuery).empty:
			logger.info('Condition satisfied!!')
			try:
				logger.info('Sending Email...')
				self.sendEmailAlert()	
			except Exception, e:
				logger.info('Email not sent...')
				raise e
			finally:
				emailSent = True
				logger.info('Email sent!')
		else:
			logger.info('No bonds today!!')

		logger.info('Saving task in DB...')
		self.saveTask(emailSent)

		return None		

	def run(self):
        
		scrapper = BondScrapper()
		self.bonds_table = scrapper.getBondTable()

		for alert in self.alerts['alerts']:
			self.alert_trigger(alert)

if __name__ == "__main__":

	alert = Alert('alerts.json')
	alert.run()
	


