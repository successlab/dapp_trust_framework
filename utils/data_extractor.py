from datetime import datetime

import pandas as pd
from math import ceil
import concurrent.futures

import logging

from utils.basic_web3.address_classifier import is_valid_eth_address, is_contract
from utils.github_crawler import get_github_all_code_search_results, check_web3js_usage_parallel

logger = logging.getLogger(__name__)


def get_w3js_use(eth_address):
    search_address = eth_address
    print("Received address: ", search_address)
    if is_valid_eth_address(search_address) is False or is_contract(search_address) is False:
        return {}

    try:
        res = get_github_all_code_search_results(search_address)
        found_web3js_import, found_metamask_trigger, web3js_uses = check_web3js_usage_parallel(res)

        out_data = {
            "status": "successful",
            "found_web3js_import": found_web3js_import,
            "found_metamask_trigger": found_metamask_trigger,
            "web3js_uses": web3js_uses,
            "all_github_code_search_results": res,
        }

        return out_data

    except:
        return {}


def process_and_save(df, out_csvs_dir_path, part_num):
    df['web3js_uses'] = pd.Series(dtype='object')
    df['all_github_code_search_results'] = pd.Series(dtype='object')

    for i in range(len(df)):
        eth_address = df.iloc[i, 0]
        resp = get_w3js_use(eth_address)

        try:
            web3js_uses = resp["web3js_uses"]
            df.iat[i, df.columns.get_loc("web3js_uses")] = web3js_uses
        except:
            pass

        try:
            all_github_code_search_results = resp["all_github_code_search_results"]
            df.iat[i, df.columns.get_loc("all_github_code_search_results")] = all_github_code_search_results
        except:
            pass

    df.to_csv(out_csvs_dir_path + "part_" + str(part_num) + ".csv", index=False)


def process_and_save_parallel(df, out_csvs_dir_path, part_num):
    logger = logging.getLogger(__name__)
    df['web3js_uses'] = pd.Series(dtype='object')
    df['all_github_code_search_results'] = pd.Series(dtype='object')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use the executor.submit() method to schedule the get_w3js_use() function to be
        # executed by a worker thread, passing in the appropriate arguments.
        future_to_address = {executor.submit(get_w3js_use, df.iat[i, df.columns.get_loc("Address")]): i for i in range(len(df))}
        for future in concurrent.futures.as_completed(future_to_address):
            i = future_to_address[future]
            try:
                resp = future.result()
                web3js_uses = resp["web3js_uses"]
                all_github_code_search_results = resp["all_github_code_search_results"]
                df.iat[i, df.columns.get_loc("web3js_uses")] = web3js_uses
                df.iat[i, df.columns.get_loc("all_github_code_search_results")] = all_github_code_search_results
            except Exception as e:
                logger.error("Error with address %s: %s", df.iat[i, df.columns.get_loc("Address")], e)

    df.to_csv(out_csvs_dir_path + "part_" + str(part_num) + ".csv", index=False)


def write_into_dataset(in_csv_path, out_csvs_dir_path, data_length=1586, chunk_size=50):
    logger = logging.getLogger(__name__)
    base_df_col_names = [
        'Address',
        'Name',
        'Label',
        'six_months_txs_raw',
        'n_transactions',
        'avg_trx_freq',
        'avg_sender_nonce',
        'avg_gas_price',
        'avg_gas_consumed',
        'median_trx_freq',
        'median_sender_nonce',
        'median_gas_price',
        'median_gas_consumed',
        'returning_user_perc',
        'n_unique_incoming_addresses',
        'n_deployer_transactions'
    ]

    limit = int(ceil(data_length/chunk_size))
    print("The limit is: ", limit)
    
    for i in range(32, limit + 2):
        print("Processing Chunk " + str(i) + " at time: " + str(datetime.now()))
        if i == 0:
            df = pd.read_csv(in_csv_path, skiprows=(i * chunk_size), nrows=chunk_size, names=base_df_col_names, header=None)

        elif i == 32:
            df = pd.read_csv(in_csv_path, skiprows=(i * chunk_size), names=base_df_col_names, header=None)

        else:
            df = pd.read_csv(in_csv_path, skiprows=(i * chunk_size), nrows=chunk_size, names=base_df_col_names, header=None)

        # process_and_save(df, out_csvs_dir_path, i)
        process_and_save(df, out_csvs_dir_path, i)
        del df

        print("Finished processing chunk " + str(i) + " at time: " + str(datetime.now()))

    print("Finished running the program")


# write_into_dataset("final_combined_df.csv", "./out_chunks/")
