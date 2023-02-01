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

	val_list = []

	val_list.append(len(transactions))
	try:
		# df.loc[0]["avg_trx_freq"] = get_avg_trx_freq(transactions)
		val_list.append(get_avg_trx_freq(transactions))
	except:
		val_list.append(-1)
	val_list.append(get_avg_gas_price(transactions))
	val_list.append(get_avg_gas_consumed(transactions))

	val_list.append(get_median_sender_nonce(transactions))

	val_list.append(get_returning_user_perc(transactions))
	val_list.append(get_n_unique_incoming_addresses(transactions))
	val_list.append(get_n_deployer_transactions(transactions))

	val_list.append(1 if contains_abi(address) else 0)

	df.loc[0] = val_list

	return df
