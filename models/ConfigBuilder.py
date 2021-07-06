"""config.json Configuration Builder"""

from json import dump
from os.path import isfile
from re import compile as re_compile
from sys import exit as sys_exit

import keyring


class ConfigBuilder():
    def __init__(self) -> None:
        self._b = 0
        self._c = 0
        self._t = 0

    def init(self) -> None:
        print("*** config.json Configuration Builder ***")

        if isfile('config.json'):
            print("config.json already exists.")
            sys_exit()

        config = {}

        choice = input(
            "Do you want to use the Coinbase Pro exchange (1=yes, 2=no:default)? ")
        if choice == '1':
            self._c = 1
            config['coinbasepro'] = {'api_url': 'https://api.pro.coinbase.com'}
            choice = input(
                "Do you have API keys for the Coinbase Pro exchange (1=yes, 2=no:default)? ")
            if choice == '1':
                api_key = None
                while 'api_key' not in config['coinbasepro']:
                    api_key = input("What is your Coinbase Pro API Key? ")
                    p = re_compile(r"^[a-f0-9]{32,32}$")
                    if p.match(api_key):
                        config['coinbasepro']['api_key'] = api_key

                while 'api_secret' not in config['coinbasepro']:
                    api_secret = input(
                        "What is your Coinbase Pro API Secret? ")
                    p = re_compile(r"^[A-z0-9+\/]+==$")
                    if p.match(api_secret):
                        config['coinbasepro']['api_secret'] = api_secret
                        keyring.set_password(
                            "pycryptobot", api_key, api_secret)
                config['coinbasepro'].pop('api_secret')

                while 'api_passphrase' not in config['coinbasepro']:
                    api_passphrase = input(
                        "What is your Coinbase Pro API Passphrase? ")
                    p = re_compile(r"^[a-z0-9]{10,11}$")
                    if p.match(api_passphrase):
                        config['coinbasepro']['api_passphrase'] = api_passphrase
            else:
                config['coinbasepro']['api_key'] = '<fill in>'
                config['coinbasepro']['api_secret'] = '<fill in>'
                config['coinbasepro']['api_passphrase'] = '<fill in>'

            config['coinbasepro']['config'] = {}

            while 'base_currency' not in config['coinbasepro']['config']:
                base_currency = input(
                    "What is your Coinbase Pro base currency (what you are buying) E.g. BTC? ")
                p = re_compile(r"^[A-Z0-9]{3,7}$")
                if p.match(base_currency):
                    config['coinbasepro']['config']['base_currency'] = base_currency

            while 'quote_currency' not in config['coinbasepro']['config']:
                quote_currency = input(
                    "What is your Coinbase Pro quote currency (what you are buying with) E.g. GBP? ")
                p = re_compile(r"^[A-Z0-9]{3,7}$")
                if p.match(quote_currency):
                    config['coinbasepro']['config']['quote_currency'] = quote_currency

            choice = input(
                "Do you want to smart switch between 1 hour and 15 minute intervals (1=yes:default, 2=no)? ")
            if choice == '2':
                while 'granularity' not in config['coinbasepro']['config']:
                    choice = input(
                        "What granularity do you want to trade? (60, 300, 900, 3600, 21600, 86400)? ")
                    if int(choice) in [60, 300, 900, 3600, 21600, 86400]:
                        config['coinbasepro']['config']['granularity'] = int(
                            choice)

            choice = input(
                "Do you want to start live trading? (1=live, 2=test:default)? ")
            config['coinbasepro']['config']['live'] = 1 if choice == '1' else 0

        choice = input(
            "Do you want to use the Binance exchange (1=yes, 2=no:default)? ")
        if choice == '1':
            self._b = 1
            config['binance'] = {'api_url': 'https://api.binance.com'}
            choice = input(
                "Do you have API keys for the Binance exchange (1=yes, 2=no:default)? ")
            if choice == '1':
                api_key = None
                while 'api_key' not in config['binance']:
                    api_key = input("What is your Binance API Key? ")
                    p = re_compile(r"^[A-z0-9]{64,64}$")
                    if p.match(api_key):
                        config['binance']['api_key'] = api_key

                while 'api_secret' not in config['binance']:
                    api_secret = input("What is your Binance API Secret? ")
                    p = re_compile(r"^[A-z0-9]{64,64}$")
                    if p.match(api_secret):
                        config['binance']['api_secret'] = api_secret
                        keyring.set_password(
                            "pycryptobot", api_key, api_secret)
                config['binance'].pop('api_secret')
            else:
                config['binance']['api_key'] = '<fill in>'
                config['binance']['api_secret'] = '<fill in>'

            config['binance']['config'] = {}

            while 'base_currency' not in config['binance']['config']:
                base_currency = input(
                    "What is your Binance base currency (what you are buying) E.g. BTC? ")
                p = re_compile(r"^[A-Z0-9]{3,7}$")
                if p.match(base_currency):
                    config['binance']['config']['base_currency'] = base_currency

            while 'quote_currency' not in config['binance']['config']:
                quote_currency = input(
                    "What is your Binance quote currency (what you are buying with) E.g. GBP? ")
                p = re_compile(r"^[A-Z0-9]{3,7}$")
                if p.match(quote_currency):
                    config['binance']['config']['quote_currency'] = quote_currency

            choice = input(
                "Do you want to smart switch between 1 hour and 15 minute intervals (1=yes:default, 2=no)? ")
            if choice == '2':
                while 'granularity' not in config['binance']['config']:
                    choice = input(
                        "What granularity do you want to trade? (1m, 5m, 15m, 1h, 6h, 1d)? ")
                    if choice in ['1m', '5m', '15m', '1h', '6h', '1d']:
                        config['binance']['config']['granularity'] = choice

            choice = input(
                "Do you want to start live trading? (1=live, 2=test:default)? ")
            config['binance']['config']['live'] = 1 if choice == '1' else 0
        if self._b == 1 or self._c == 1:
            choice = input(
                "Do you have a Telegram Token and Client ID (1=yes, 2=no:default)? ")
            if choice == '1':
                self._t = 1
                config['telegram'] = {}

                client_id = None
                while 'client_id' not in config['telegram']:
                    client_id = input("What is your Telegram client ID? ")
                    p = re_compile(r"^-*\d{7,10}$")
                    if p.match(client_id):
                        config['telegram']['client_id'] = client_id

                while 'token' not in config['telegram']:
                    token = input("What is your Telegram token? ")
                    p = re_compile(r"^\d{1,10}:[A-z0-9-_]{35,35}$")
                    if p.match(token):
                        config['telegram']['token'] = token
                        keyring.set_password("pycryptobot", client_id, token)
                config['telegram'].pop('token')

            choice = input(
                "Do you want to ever sell at a loss even to minimise losses (1:yes, 2=no:default)? ")
            if choice == '1':
                if self._c == 1:
                    config['coinbasepro']['config']['sellatloss'] = 1
                if self._b == 1:
                    config['binance']['config']['sellatloss'] = 1

            choice = input(
                "Do you want to sell at the next resistance? (1:yes:default, 2=no)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['sellatresistance'] = 1
                if self._b == 1:
                    config['binance']['config']['sellatresistance'] = 1

            choice = input(
                "Do you only want to trade in a bull market SMA50 > SMA200? (1:yes, 2=no:default)? ")
            if choice != '1':
                if self._c == 1:
                    config['coinbasepro']['config']['disablebullonly'] = 1
                if self._b == 1:
                    config['binance']['config']['disablebullonly'] = 1

            choice = input(
                "Do you want to avoid buying when the price is too high? (1:yes:default, 2=no)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['disablebuynearhigh'] = 1
                if self._b == 1:
                    config['binance']['config']['disablebuynearhigh'] = 1

            choice = input(
                "Do you want to disable the On-Balance Volume (OBV) technical indicator on buys? (1:yes:default, 2=no)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['disablebuyobv'] = 1
                if self._b == 1:
                    config['binance']['config']['disablebuyobv'] = 1

            choice = input(
                "Do you want to disable the Elder-Ray Index on buys? (1:yes:default, 2=no)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['disablebuyelderray'] = 1
                if self._b == 1:
                    config['binance']['config']['disablebuyelderray'] = 1

            choice = input(
                "Do you want to disable saving the CSV tracker on buy and sell events? (1:yes:default, 2=no)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['disabletracker'] = 1
                if self._b == 1:
                    config['binance']['config']['disabletracker'] = 1

            choice = input(
                "Do you want to disable writing to the log file? (1:yes, 2=no:default)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['disablelog'] = 1
                if self._b == 1:
                    config['binance']['config']['disablelog'] = 1

            choice = input(
                "Do you want the bot to auto restart itself on failure? (1:yes:default, 2=no)? ")
            if choice != '2':
                if self._c == 1:
                    config['coinbasepro']['config']['autorestart'] = 1
                if self._b == 1:
                    config['binance']['config']['autorestart'] = 1

            try:
                with open('./config.json', 'w') as file_out:
                    dump(config, file_out, indent=4)
                print("config.json saved!")
            except Exception as err:
                print(err)
        else:
            print('You have to select the exchange you want to use.')

        return None
