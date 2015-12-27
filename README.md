# Tesouro Investor

Create alerts to help you monitor Tesouro Direto yield rates and help you to invest your money at the right time! This project starts as simple buy alerts but intents to evolve as a general support tool for Tesouro Direto investors.  

## Configuration

1. `pip install tesouro-investor` (not yet)
1. Create DB
1. Run cron.sh to include cron

### Useful Cron Tab commands
* **Set up crontab:** crontab -e
* **Show crontab:** crontab -l 

### Next Steps
* implement cli with argparse
* load alerts.json from root
* treat "No internet connection" Exception
* organize structure to publish in pypi
* add README.rst
* add setup.py
* use jinja2 to send e-mails
* tests for exceptions in Email send process
