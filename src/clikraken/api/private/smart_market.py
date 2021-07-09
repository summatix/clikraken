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
VOLUME_DECIMALS = 12


def _get_mid_price(pair, args, round_to_decimals = 2):
    """Gets the latest mid price for a pair."""
    res = query_api('public', 'Depth', {
        'pair': pair,
        'count': 1
    }, args)

    ask = res[pair]['asks'][0][0]
    bid = res[pair]['bids'][0][0]
    return round((Decimal(ask) + Decimal(bid)) / 2, round_to_decimals)


def _place_order(pair, price, amount, validate, args):
    """Place an order for the given pair."""
    volume = round(Decimal(amount) / price, VOLUME_DECIMALS)

    api_params = {
        'expiretm': '+{}'.format(ORDER_EXPIRATION_SECONDS),
        'ordertype': 'limit',
        'pair': pair,
        'price': price,
        'type': 'buy',
        'volume': volume
    }

    if validate:
        api_params['validate'] = 'true'

    res = query_api('private', 'AddOrder', api_params, args)
    logger.info(res.get('descr').get('order', 'No description available!'))

    txid = res.get('txid')

    if not txid:
        if validate:
            logger.info('Validating inputs only. Order not submitted!')
        else:
            logger.warn('Order was NOT successfully added!')

        return ""

    txid = txid[0]
    logger.info("Placed order %s", txid)
    return txid


def smart_market(args):
    """Place a smart market order."""
    mid = _get_mid_price(args.pair, args)
    txid = _place_order(args.pair, mid, args.amount, args.validate, args)
    if not txid:
        return

    # Wait for order to close
    while True:
        time.sleep(SECONDS_BETWEEN_STATUS_CHECKS)

        res = query_api('private', 'ClosedOrders', {}, args)

        if txid in res['closed'].keys():
            logger.info('Trade was closed')
            return
