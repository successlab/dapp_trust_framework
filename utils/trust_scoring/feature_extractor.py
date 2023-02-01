import pandas as pd

from .abi_availability_checker import contains_abi
from .model_features import features_and_pandas_dtypes
from .transactions_summarizer.mean_summarizers import get_avg_trx_freq, get_avg_gas_price, get_avg_gas_consumed
from .transactions_summarizer.median_summarizers import get_median_sender_nonce
from .transactions_summarizer.user_stats import get_returning_user_perc, get_n_unique_incoming_addresses, \
	get_n_deployer_transactions
from ..extractors.etherscan_extractor import get_all_transactions_until_limit


def get_features_df(address):
	# Creating a pandas dataframe
	df = pd.DataFrame()

	# Setting the feature columns
	for feature, pd_dtype in features_and_pandas_dtypes.items():
		df[feature] = pd.Series(dtype=pd_dtype)

	# Populating the dataframe
	df = fill_in_features(df, address)

	# Returning the populated pandas dataframe
	return df


def fill_in_features(df, address, transaction_len_limit=6):
	transactions = get_all_transactions_until_limit(address, transaction_len_limit)

	df.iat[0, df.columns.get_loc("n_transactions")] = len(transactions)
	try:
		df.iat[0, df.columns.get_loc("avg_trx_freq")] = 1 / get_avg_trx_freq(transactions)
	except:
		pass
	df.iat[0, df.columns.get_loc("avg_gas_price")] = get_avg_gas_price(transactions)
	df.iat[0, df.columns.get_loc("avg_gas_consumed")] = get_avg_gas_consumed(transactions)

	df.iat[0, df.columns.get_loc("median_sender_nonce")] = get_median_sender_nonce(transactions)

	df.iat[0, df.columns.get_loc("returning_user_perc")] = get_returning_user_perc(transactions)
	df.iat[0, df.columns.get_loc("n_unique_incoming_addresses")] = get_n_unique_incoming_addresses(transactions)
	df.iat[0, df.columns.get_loc("n_deployer_transactions")] = get_n_deployer_transactions(transactions)

	df.iat[0, df.columns.get_loc("contains_abi")] = contains_abi(address)

	return df
