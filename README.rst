Tesouro Investor
==============

This project starts as simple buy alerts but intents to evolve as a general support tool for Tesouro Direto investors.

Package 1 - Alerts: Create alerts to help you to monitor Tesouro Direto yield rates and to invest your money at the right time! 

Package 2 - Market Expectations (working): What to yield curves can tell us about market expectations regarding SELIC rates? 

Package 3 - Manage your Portfolio (working): How much money are you making? What are the best bonds for you to sell?

Installation
------------

To install the tool the easiest way is to use pip::

    pip install tesouro-direto (not yet)

Configuration
-------------

config.yml sample with e-mail credentials:

.. code-block:: YAML

    # SMTP settings for email sending. If port is not specified, the default
    # value is 25. Provide the username and password if necessary.
    smtp:
        server: "mail.mydomain.com"
        port: 587
        username: "user"
        password: "secret"

        from: "me@mydomain.com"
        to: "you@yourdomain.com"


* Create DB

Usage
-------------

Invoke installed python module from terminal with the followign command: 

    python -m tesouro_investor.alert -c config.yml

Configuring Crontab (Linux)
^^^^^^^^^^^^^^^^^^^

You can configure crontab to call the program above. This way you can have a automated email at the time and periodicity that you like.

Add to crontab with bash script
* Run cron.sh to include default cron

Add manually using:
* **Set up crontab:** crontab -e
* **Show crontab:** crontab -l 

Next Steps
-------------

* start using issues instead of readme lol
* implement cli with argparse or other
* organize structure to publish in pypi
    * Finish setup.py
    * Finish setup.cfg
    * Finish README.rst
* support python 3
* load alerts.json from root (include in MANIFEST.in)
* treat "No internet connection" Exception
* use jinja2 to send e-mails
* tests for exceptions in Email send process
