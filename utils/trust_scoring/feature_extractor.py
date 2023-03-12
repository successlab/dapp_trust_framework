import pandas as pd

from django.conf import settings

from trust_scoring.models import ContractFeatures
from .abi_availability_checker import contains_abi
from .model_features import features_and_pandas_dtypes
from .transactions_summarizer.mean_summarizers import get_avg_trx_freq, get_avg_gas_price, get_avg_gas_consumed
from .transactions_summarizer.median_summarizers import get_median_sender_nonce
from .transactions_summarizer.user_stats import get_returning_user_perc, get_n_unique_incoming_addresses, \
	get_n_deployer_transactions
from ..extractors.etherscan_extractor import get_all_transactions_until_limit
from ..github_crawler import get_github_all_code_search_results, check_web3js_usage_parallel


def get_features_df(address):
	# Creating a pandas dataframe
	df = pd.DataFrame()

	# Setting the feature columns
	for feature, pd_dtype in features_and_pandas_dtypes.items():
		df[feature] = pd.Series(dtype=pd_dtype)

	# Checking if the features already exist
	if ContractFeatures.objects.filter(contract__address__eth_address=address).exists():
		df, web3js_uses, trust_score = fill_in_features_from_db(df, address)
		return df, web3js_uses, trust_score

	else:
		# Populating the dataframe
		df, web3js_uses = fill_in_features(df, address)
		return df, web3js_uses, None


def fill_in_features_from_db(df, address):
	features_obj = ContractFeatures.objects.get(contract__address__eth_address=address)

	val_list = []
	# val_list.append(features_obj.n_transactions)
	val_list.append(features_obj.avg_trx_freq)
	val_list.append(features_obj.avg_gas_price)
	val_list.append(features_obj.avg_gas_consumed)
	val_list.append(features_obj.median_sender_nonce)
	val_list.append(features_obj.returning_user_perc)
	val_list.append(features_obj.n_unique_incoming_addresses)
	val_list.append(features_obj.n_deployer_transactions)
	val_list.append(features_obj.contains_abi)
	try:
		val_list.append(1 if len(features_obj.web3js_uses) > 0 else 0)
	except:
		val_list.append(0)

	df.loc[0] = val_list

	try:
		web3js_uses = features_obj.web3js_uses
	except:
		web3js_uses = []

	trust_score = features_obj.trust_score

	return df, web3js_uses, trust_score


def fill_in_features(df, address):
	transaction_len_limit = settings.TRANSACTIONS_LIMIT_IN_MONTHS
	transactions = get_all_transactions_until_limit(address, transaction_len_limit)

	val_list = []

	# val_list.append(len(transactions))

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

	try:
		w3js_import_val, web3js_uses = get_w3js_uses(address)
		val_list.append(1 if (len(web3js_uses) > 0) else 0)
	except:
		web3js_uses = []
		val_list.append(0)

	df.loc[0] = val_list

	return df, web3js_uses


def get_w3js_uses(address):
	res = get_github_all_code_search_results(address)
	found_web3js_import, found_metamask_trigger, web3js_uses = check_web3js_usage_parallel(res)

	return found_web3js_import, web3js_uses
