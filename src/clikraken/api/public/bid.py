# -*- coding: utf8 -*-

"""
clikraken.api.public.bid

This module queries the Depth method of Kraken's API
and outputs the latest bid price.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from decimal import Decimal

from clikraken.api.api_utils import query_api


def bid(args):
    """Get the latest bid price."""

    # Parameters to pass to the API
    api_params = {
        'pair': args.pair,
        'count': 1
    }

    res = query_api('public', 'Depth', api_params, args)

    print(str.rstrip(res[args.pair]['bids'][0][0], '0'))
