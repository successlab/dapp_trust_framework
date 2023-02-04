def get_returning_user_perc(tx_list):
    if len(tx_list) == 0:
        # TODO: Handle this case
        return None

    user_tx_count = {}

    for tx in tx_list:
        sender_address = tx["from"]
        user_tx_count[sender_address] = user_tx_count.get(sender_address, 0) + 1

    n_returning_users = 0
    for v in user_tx_count.values():
        user_tx_freq = v
        if user_tx_freq > 1:
            n_returning_users += 1

    n_users = len(user_tx_count)
    del user_tx_count

    return (n_returning_users / n_users) * 100


def get_n_unique_incoming_addresses(tx_list):
    incoming_addresses = set()
    for tx in tx_list:
        incoming_addresses.add(tx['from'])

    return len(incoming_addresses)


def get_n_deployer_transactions(tx_list):
    deployer = tx_list[0]['from']
    n_deployer_transactions = 0

    for tx in tx_list:
        if tx['from'] == deployer:
            n_deployer_transactions += 1

    return n_deployer_transactions
