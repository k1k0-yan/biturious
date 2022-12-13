from binance.client import Client
import os
import sys


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")


if os.path.exists('settings.txt'):
    file = open('settings.txt', 'r')
    data = file.readlines()
    try:
        apikey = data[2].strip()
        secretkey = data[3].strip()
        apikey = apikey[apikey.find('=') + 1:]
        secretkey = secretkey[secretkey.find('=') + 1:]
    except:
        apikey = ''
        secretkey = ''
else:
    apikey = ''
    secretkey = ''

# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()

client = Client(
    apikey,
    secretkey
)
