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

Set up your alerts in a alerts.json file in the following format:

.. code-block:: javascript

    {
        "alerts":[{
            "bound_name":"NTNB Princ",
            "expiration":"2035", ##not used yet
            "yield":"7.5"
        },
        {
            "bound_name":"LTN",
            "expiration":"2018", ##not used yet
            "yield":"16.6"
        }]
    }


* Create DB

Usage
-------------

Use cli interface to trigger aler command passing as arguments the `config.yml` and `alerts.json`

    tinvest alert config.yml alerts.json

Configuring Crontab (Linux)
^^^^^^^^^^^^^^^^^^^

You can configure crontab to call the program above. This way you can have a automated email at the time and periodicity that you like.

Add to crontab with bash script
* Run cron.sh to include default cron

Add manually using:
* **Set up crontab:** crontab -e
* **Show crontab:** crontab -l 
