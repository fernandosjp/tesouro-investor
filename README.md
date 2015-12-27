# Tesouro Investor

## Configuration

1. `pip install tesouro-investor`
1. Create DB
1. Run cron.sh to include cron

### Useful Cron Tab commands
* **Set up crontab:** crontab -e
* **Show crontab:** crontab -l 

### Next Steps
* load yml config for e-mail params
* implement cli with argparse
* load alerts.json from root
* change subject of email according with alert
* organize structure to publish in pypi
* add README.rst
* add setup.py
* use jinja2 to send e-mails
* treat "No internet connection" Exception
* tests for exceptions in Email send process
