import json
from celery import shared_task
from datetime import timedelta
import pandas as pd

from trust_scoring.models import ContractFeatures
from contract_relations.models import Contract, Address

@shared_task
def write_features_df_into_db(address, features_df_json, is_proxy=False, contract_name="", web3js_uses_dict=None, n_months=6, trust_score=None):
	if web3js_uses_dict is not None:
		web3js_uses_dict = web3js_uses_dict

	if contract_name is None:
		contract_name = ""

	features_df = pd.read_json(features_df_json)

	if len(features_df) == 0:
		return


	# Checking if the object already exists
	term_len_to_check = timedelta(days=183 if n_months == 6 else (n_months * 31))
	pre_existing = ContractFeatures.objects.filter(
		contract__address__eth_address=address,
		term_length=term_len_to_check
	)

	if len(pre_existing) > 0:
		return

	try:
		contract_obj = Contract.objects.get(address__eth_address=address)
	except:
		address_obj = Address.objects.get_or_create(
			eth_address=address,
			type="Contract",
		)

		contract_obj = Contract.objects.get_or_create(
			address=address_obj[0],
			name=contract_name,
			is_proxy=is_proxy,
		)[0]

	if ContractFeatures.objects.filter(contract=contract_obj).exists():
		return

	contract_features = ContractFeatures()
	contract_features.contract = contract_obj

	if n_months != 6:
		contract_features.term_length = timedelta(days=(n_months * 31))

	# contract_features.n_transactions = features_df.iloc[0]["n_transactions"]
	contract_features.avg_trx_freq = features_df.iloc[0]["avg_trx_freq"]
	contract_features.avg_gas_price = features_df.iloc[0]["avg_gas_price"]
	contract_features.avg_gas_consumed = features_df.iloc[0]["avg_gas_consumed"]
	contract_features.median_sender_nonce = features_df.iloc[0]["median_sender_nonce"]
	contract_features.returning_user_perc = features_df.iloc[0]["returning_user_perc"]
	contract_features.n_unique_incoming_addresses = features_df.iloc[0]["n_unique_incoming_addresses"]
	contract_features.n_deployer_transactions = features_df.iloc[0]["n_deployer_transactions"]
	contract_features.contains_abi = features_df.iloc[0]["contains_abi"]
	contract_features.web3js_uses = web3js_uses_dict

	if trust_score is not None:
		contract_features.trust_score = trust_score

	contract_features.save()
