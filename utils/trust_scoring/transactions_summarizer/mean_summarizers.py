from datetime import datetime
from math import ceil


def get_n_transactions(tx_list):
    return len(tx_list)


def get_avg_trx_freq(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return -1

    prev_ts = int(tx_list[0]['timeStamp'])
    total_freq = -1
    # TODO: Make sure to handle the case where there is only one transaction

    for i in range(1, len(tx_list)):
        next_ts = int(tx_list[i]['timeStamp'])
        time_delta = (datetime.fromtimestamp(next_ts) - datetime.fromtimestamp(prev_ts)).total_seconds()
        if total_freq == -1:
            total_freq = time_delta
        else:
            total_freq += time_delta

        prev_ts = next_ts

    if total_freq != -1:
        return 1/(total_freq / (len(tx_list) - 1))
    else:
        return -1


def get_avg_sender_nonce(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return -1

    total_nonce = 0

    for tx in tx_list:
        nonce = int(tx['nonce'])
        total_nonce += nonce

    return int(ceil(total_nonce / len(tx_list)))


def get_avg_gas_price(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return -1

    total_gas_price = 0

    for tx in tx_list:
        total_gas_price += int(tx['gasPrice'])

    return total_gas_price / len(tx_list)


def get_avg_gas_consumed(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return -1

    total_gas_consumed = 0

    for tx in tx_list:
        total_gas_consumed += int(tx['gasUsed'])

    return total_gas_consumed / len(tx_list)
