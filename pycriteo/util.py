#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json


class CurrencyConverter(object):
    """
    Converts currencies (ISO 4217 format).

    Arguments:
        from_currency -- currency to convert from (i.e 'EUR')
        to_currency  -- currency to convert to (i.e 'USD')

    Example:
        Convert from USD to EUR

        >>> currency_converter = CurrencyConverter('USD', 'EUR')
        >>> currency_converter.convert(45.15)
        33.34
    """


    def __init__(self, from_currency, to_currency):
        _from = from_currency.upper()
        _to = to_currency.upper()
        if len(_from) != 3 or len(_to) != 3:
            raise Exception("Currency has wrong length (should have length 3)")
        self.from_currency = _from
        self.to_currency = _to
        self.exchange_rate = None

    def convert(self, amount):
        return round(float(amount) * float(self._exchange_rate()), 2)

    def _exchange_rate(self):
        if not self.exchange_rate:
            self.exchange_rate = self._get_exchange_rate()
        return self.exchange_rate

    def _get_exchange_rate(self):
        request_url = ("http://rate-exchange.appspot.com/currency?"
                       "from={0}&to={1}".format(self.from_currency,
                                                 self.to_currency))
        response = urllib2.urlopen(request_url)
        exchange_info = json.loads(response.read())
        if 'err' in exchange_info:
            raise Exception(exchange_info['err'] +
                           " Check if your currencies are in ISO 4217")

        assert(exchange_info['to'] == self.to_currency)
        assert(exchange_info['from'] == self.from_currency)
        return exchange_info['rate']


