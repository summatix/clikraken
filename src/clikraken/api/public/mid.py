# -*- coding: utf8 -*-

"""
clikraken.api.public.mid

This module queries the Depth method of Kraken's API
and outputs the latest mid price.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from decimal import Decimal

from clikraken.api.api_utils import query_api


def mid(args):
    """Get the latest mid price."""

    # Parameters to pass to the API
    api_params = {
        'pair': args.pair,
        'count': 1
    }

    res = query_api('public', 'Depth', api_params, args)

    ask = res[args.pair]['asks'][0][0]
    bid = res[args.pair]['bids'][0][0]
    mid = round((Decimal(ask) + Decimal(bid)) / 2, 2)
    print(mid)
