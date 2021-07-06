from models.helper.LogHelper import Logger
from models.exchange.binance import AuthAPI, PublicAPI
import json
import os
import sys
from datetime import datetime

import keyring
import pandas
import pytest
import urllib3

# disable insecure ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.append(".")
# pylint: disable=import-error
Logger.configure()


# there is no dynamic way of retrieving a valid order market
VALID_ORDER_MARKET = "DOGEUSDT"


def get_api_settings(filename):
    with open(filename) as config_file:
        config = json.load(config_file)
    api_key = ""
    api_secret = ""
    api_url = ""
    if "api_key" in config and "api_pass" in config and "api_url" in config:
        api_key = config["api_key"]
        api_secret = keyring.get_password("pycryptobot", api_key)
        api_url = config["api_url"]
    elif "api_key" in config["binance"] and "api_url" in config["binance"]:
        api_key = config["binance"]["api_key"]
        api_secret = keyring.get_password("pycryptobot", api_key)
        api_url = config["binance"]["api_url"]
    return {api_key, api_secret, api_url}


def test_instantiate_authapi_without_error():
    api_key = "0000000000000000000000000000000000000000000000000000000000000000"
    api_secret = "0000000000000000000000000000000000000000000000000000000000000000"
    exchange = AuthAPI(api_key, api_secret)
    assert isinstance(exchange, AuthAPI)


def test_instantiate_authapi_with_api_key_error():
    api_key = "ERROR"
    api_secret = "0000000000000000000000000000000000000000000000000000000000000000"

    with pytest.raises(SystemExit) as execinfo:
        AuthAPI(api_key, api_secret)
    assert str(execinfo.value) == "Binance API key is invalid"


def test_instantiate_authapi_with_api_secret_error():
    api_key = "0000000000000000000000000000000000000000000000000000000000000000"
    api_secret = "ERROR"

    with pytest.raises(SystemExit) as execinfo:
        AuthAPI(api_key, api_secret)
    assert str(execinfo.value) == "Binance API secret is invalid"


def test_instantiate_authapi_with_api_url_error():
    api_key = "0000000000000000000000000000000000000000000000000000000000000000"
    api_secret = "0000000000000000000000000000000000000000000000000000000000000000"
    api_url = "ERROR"

    with pytest.raises(ValueError) as execinfo:
        AuthAPI(api_key, api_secret, api_url)
    assert str(execinfo.value) == "Binance API URL is invalid"


def test_instantiate_publicapi_without_error():
    exchange = PublicAPI()
    assert isinstance(exchange, PublicAPI)


def test_config_json_exists_and_valid():
    filename = "config.json"
    assert os.path.exists(filename) is True
    (api_key, api_secret, api_url) = get_api_settings(filename)
    AuthAPI(api_key, api_secret, api_url)


def test_getAccount():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getAccount()
    assert isinstance(df, pandas.core.frame.DataFrame)

    actual = df.columns.to_list()
    expected = ["currency", "balance", "hold", "available"]
    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(actual, expected))


def test_getFeesWithoutMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getFees()
    assert isinstance(df, pandas.core.frame.DataFrame)

    assert len(df) > 1

    actual = df.columns.to_list()
    expected = ["maker_fee_rate", "taker_fee_rate", "usd_volume", "market"]
    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(actual, expected))


def test_getFeesWithMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getFees(VALID_ORDER_MARKET)
    assert isinstance(df, pandas.core.frame.DataFrame)

    assert len(df) == 1

    actual = df.columns.to_list()
    expected = ["maker_fee_rate", "taker_fee_rate", "usd_volume", "market"]
    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(actual, expected))


def test_getTakerFeeWithoutMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    fees = exchange.getTakerFee()
    assert type(fees) is pandas.core.frame.DataFrame
    assert len(fees) > 0


def test_getTakerFeeWithMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    fee = exchange.getTakerFee(VALID_ORDER_MARKET)
    assert isinstance(fee, float)
    assert fee > 0


def test_getMakerFeeWithoutMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    fees = exchange.getMakerFee()
    assert type(fees) is pandas.core.frame.DataFrame
    assert len(fees) > 0


def test_getMakerFeeWithMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    fee = exchange.getMakerFee(VALID_ORDER_MARKET)
    assert isinstance(fee, float)
    assert fee > 0


def test_getOrders():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(VALID_ORDER_MARKET)

    assert len(df) > 0

    actual = df.columns.to_list()
    expected = [
        "created_at",
        "market",
        "action",
        "type",
        "size",
        "filled",
        "status",
        "price",
    ]
    #  order is not important, but no duplicate
    assert len(actual) == len(expected)
    diff = set(actual) ^ set(expected)
    assert not diff


def test_getOrdersInvalidMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    with pytest.raises(ValueError) as execinfo:
        exchange.getOrders(market="ERROR")
    assert str(execinfo.value) == "Binance market is invalid."


def test_getOrdersValidMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET)

    assert len(df) > 0

    actual = df.columns.to_list()
    expected = [
        "created_at",
        "market",
        "action",
        "type",
        "size",
        "filled",
        "status",
        "price",
    ]
    #  order is not important, but no duplicate
    assert len(actual) == len(expected)
    diff = set(actual) ^ set(expected)
    assert not diff


def test_getOrdersInvalidAction():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    with pytest.raises(ValueError) as execinfo:
        exchange.getOrders(action="ERROR")
    assert str(execinfo.value) == "Invalid order action."


def test_getOrdersValidActionBuy():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, action="buy")

    assert len(df) >= 0

    actual = df.columns.to_list()
    expected = [
        "created_at",
        "market",
        "action",
        "type",
        "size",
        "filled",
        "status",
        "price",
    ]
    #  order is not important, but no duplicate
    assert len(actual) == len(expected)
    diff = set(actual) ^ set(expected)
    assert not diff


def test_getOrdersValidActionSell():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, action="sell")

    assert len(df) >= 0

    actual = df.columns.to_list()
    expected = [
        "created_at",
        "market",
        "action",
        "type",
        "size",
        "filled",
        "status",
        "price",
    ]
    #  order is not important, but no duplicate
    assert len(actual) == len(expected)
    diff = set(actual) ^ set(expected)
    assert not diff


def test_getOrdersInvalidStatus():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    with pytest.raises(ValueError) as execinfo:
        exchange.getOrders(status="ERROR")
    assert str(execinfo.value) == "Invalid order status."


def test_getOrdersValidStatusAll():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, status="all")

    if len(df) != 0:
        actual = df.columns.to_list()
        expected = [
            "created_at",
            "market",
            "action",
            "type",
            "size",
            "filled",
            "status",
            "price",
        ]
        #  order is not important, but no duplicate
        assert len(actual) == len(expected)
        diff = set(actual) ^ set(expected)
        assert not diff


def test_getOrdersValidStatusOpen():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, status="open")

    if len(df) != 0:
        actual = df.columns.to_list()
        expected = [
            "created_at",
            "market",
            "action",
            "type",
            "size",
            "filled",
            "status",
            "price",
        ]
        #  order is not important, but no duplicate
        assert len(actual) == len(expected)
        diff = set(actual) ^ set(expected)
        assert not diff


def test_getOrdersValidStatusPending():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, status="pending")

    if len(df) != 0:
        actual = df.columns.to_list()
        expected = [
            "created_at",
            "market",
            "action",
            "type",
            "size",
            "filled",
            "status",
            "price",
        ]
        #  order is not important, but no duplicate
        assert len(actual) == len(expected)
        diff = set(actual) ^ set(expected)
        assert not diff


def test_getOrdersValidStatusDone():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, status="done")

    if len(df) != 0:
        actual = df.columns.to_list()
        expected = [
            "created_at",
            "market",
            "action",
            "type",
            "size",
            "filled",
            "status",
            "price",
        ]
        #  order is not important, but no duplicate
        assert len(actual) == len(expected)
        diff = set(actual) ^ set(expected)
        assert not diff


def test_getOrdersValidStatusActive():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    df = exchange.getOrders(market=VALID_ORDER_MARKET, status="active")

    if len(df) != 0:
        actual = df.columns.to_list()
        expected = [
            "created_at",
            "market",
            "action",
            "type",
            "size",
            "filled",
            "status",
            "price",
        ]
        #  order is not important, but no duplicate
        assert len(actual) == len(expected)
        diff = set(actual) ^ set(expected)
        assert not diff


def test_getTime():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    resp = exchange.getTime()
    assert type(resp) is datetime


def test_marketBuyInvalidMarket():
    filename = "config.json"
    (api_key, api_secret, api_url) = get_api_settings(filename)
    exchange = AuthAPI(api_key, api_secret, api_url)
    assert isinstance(exchange, AuthAPI)

    with pytest.raises(ValueError) as execinfo:
        exchange.marketBuy("ERROR", -1)
    assert str(execinfo.value) == "Binance market is invalid."
