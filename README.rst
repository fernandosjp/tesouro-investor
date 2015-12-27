Tesouro Investor
==============

Create alerts to help you monitor Tesouro Direto yield rates and help you to invest your money at the right time! This project starts as simple buy alerts but intents to evolve as a general support tool for Tesouro Direto investors.  

Installation
------------

To install the tool the easiest way is to use pip::

    pip install tesouro-direto (not yet)

Configuration
-------------

1. `pip install tesouro-investor` (not yet)
1. Create DB
1. Run cron.sh to include cron

Configuring Crontab
^^^^^^^^^^^^^^^^^^^

You can configure crontab to call the program above. This way you can have a automated email at the time and periodicity that you like.

* **Set up crontab:** crontab -e
* **Show crontab:** crontab -l 

Next Steps
-------------

* organize structure to publish in pypi
	* Finish setup.py
	* Finish setup.cfg
	* Finish README.rst
* implement cli with argparse
* support python 3
* load alerts.json from root
* treat "No internet connection" Exception
* add README.rst
* add setup.py
* use jinja2 to send e-mails
* tests for exceptions in Email send process
