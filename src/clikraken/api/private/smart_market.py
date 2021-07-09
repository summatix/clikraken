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


MID_POSITION_INCREMENT = 10
MINIMUM_PURCHASE = 2
ORDER_EXPIRATION_SECONDS = 30
SECONDS_BETWEEN_STATUS_CHECKS = 5
STARTING_MID_POSITION = 50
VOLUME_DECIMALS = 12


def _get_mid_price(pair, mid_position, args, round_to_decimals = 2):
    """Gets the latest mid price for a pair."""
    res = query_api('public', 'Depth', {
        'pair': pair,
        'count': 1
    }, args)

    ask = Decimal(res[pair]['asks'][0][0])
    bid = Decimal(res[pair]['bids'][0][0])

    return round(
        bid + ((ask - bid) * Decimal(mid_position / 100)),
        round_to_decimals
    )


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
    mid_position = STARTING_MID_POSITION
    amount_to_buy = Decimal(args.amount)

    # Place the first order
    mid = _get_mid_price(args.pair, mid_position, args)
    txid = _place_order(args.pair, mid, amount_to_buy, args.validate, args)
    if not txid:
        return

    # Wait for purchase to complete
    while True:
        time.sleep(SECONDS_BETWEEN_STATUS_CHECKS)

        res = query_api('private', 'ClosedOrders', {}, args)

        if txid in res['closed'].keys():
            purchased = Decimal(res['closed'][txid]["cost"])
            if purchased > 0:
                logger.info("Purchased %s of %s", purchased, args.pair)

            else:
                logger.info("Trade was closed without purchase")

            amount_to_buy = amount_to_buy - purchased

            if amount_to_buy <= MINIMUM_PURCHASE:
                return

            # Place another order at a higher mid price
            mid_position = mid_position + MID_POSITION_INCREMENT
            mid = _get_mid_price(args.pair, mid_position, args)
            txid = _place_order(args.pair, mid, amount_to_buy, args.validate, args)
            if not txid:
                return
