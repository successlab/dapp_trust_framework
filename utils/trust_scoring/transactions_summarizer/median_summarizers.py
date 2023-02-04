import statistics
from datetime import datetime


def get_median_trx_freq(tx_list):
    if len(tx_list) == 0:
        return -1

    prev_ts = int(tx_list[0]['timeStamp'])
    intervals = []

    for i in range(1, len(tx_list)):
        next_ts = int(tx_list[i]['timeStamp'])
        time_delta = (datetime.fromtimestamp(next_ts) - datetime.fromtimestamp(prev_ts)).total_seconds()
        intervals.append(time_delta)

        prev_ts = next_ts

    if len(intervals) != 0:
        intervals = sorted(intervals)

        med = statistics.median(intervals)
        del intervals
        return med

    else:
        # TODO: Handle this case
        return None


def get_median_sender_nonce(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return None

    nonces = []

    for tx in tx_list:
        nonce = int(tx['nonce'])
        nonces.append(nonce)

    med = statistics.median(nonces)
    del nonces
    return med


def get_median_gas_price(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return None

    gas_prices = []

    for tx in tx_list:
        gas_prices.append(int(tx['gasPrice']))

    med = statistics.median(gas_prices)
    del gas_prices
    return med


def get_median_gas_consumed(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return None

    gas_consumptions = []

    for tx in tx_list:
        gas_consumptions.append(int(tx['gasUsed']))

    med = statistics.median(gas_consumptions)
    del gas_consumptions
    return med
