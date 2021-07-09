# -*- coding: utf8 -*-

"""
clikraken.api.private.smart_market

This module submits a limit order at the latest mid price.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import time

from decimal import Decimal

from clikraken.api.api_utils import query_api
from clikraken.log_utils import logger


ORDER_EXPIRATION_SECONDS = 30
SECONDS_BETWEEN_STATUS_CHECKS = 5


def smart_market(args):
    """Place a smart market order."""

    res = query_api('public', 'Depth', {
        'pair': args.pair,
        'count': 1
    }, args)

    ask = res[args.pair]['asks'][0][0]
    bid = res[args.pair]['bids'][0][0]
    mid = round((Decimal(ask) + Decimal(bid)) / 2, 2)

    volume = round(Decimal(args.amount) / mid, 12)

    api_params = {
        'expiretm': '+{}'.format(ORDER_EXPIRATION_SECONDS),
        'ordertype': 'limit',
        'pair': args.pair,
        'price': mid,
        'type': 'buy',
        'volume': volume
    }

    if args.validate:
        api_params['validate'] = 'true'

    logger.info('Placing buy order of %s %s at limit %s', volume, args.pair, mid)

    res = query_api('private', 'AddOrder', api_params, args)

    descr = res.get('descr')
    odesc = descr.get('order', 'No description available!')
    print(odesc)

    txid = res.get('txid')

    if not txid:
        if args.validate:
            logger.info('Validating inputs only. Order not submitted!')
        else:
            logger.warn('Order was NOT successfully added!')

        return

    txid = txid[0]
    logger.info("Placed order %s", txid)

    # Wait for order to close
    while True:
        time.sleep(SECONDS_BETWEEN_STATUS_CHECKS)

        res = query_api('private', 'ClosedOrders', {}, args)

        if txid in res['closed'].keys():
            logger.info('Trade was closed')
            return
