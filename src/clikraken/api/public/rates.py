# -*- coding: utf8 -*-

"""
clikraken.api.public.rates

This module queries pulls the latest change rates for a currency pair.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from forex_python.converter import CurrencyRates


def rates(args):
    """Get the exchange rate for a given currency pair."""
    print(CurrencyRates().get_rate(args.from_currency, args.to_currency))
