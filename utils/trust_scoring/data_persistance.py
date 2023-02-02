from datetime import timedelta

from trust_scoring.models import ContractFeatures
from contract_relations.models import Contract, Address


def write_features_df_into_db(address, features_df, n_months=6, trust_score=None):
	if len(features_df) == 0:
		return

	contract_features = ContractFeatures()

	try:
		contract_obj = Contract.objects.get(address__eth_address=address)
	except:
		address_obj = Address()
		address_obj.eth_address = address
		address_obj.type = "Contract"
		address_obj.save()

		contract_obj = Contract()
		contract_obj.address = address_obj
		contract_obj.save()

	contract_features.contract = contract_obj

	if n_months != 6:
		contract_features.term_length = timedelta(days=(n_months * 30))

	contract_features.n_transactions = features_df.iloc[0]["n_transactions"]
	contract_features.avg_trx_freq = features_df.iloc[0]["avg_trx_freq"]
	contract_features.avg_gas_consumed = features_df.iloc[0]["avg_gas_consumed"]
	contract_features.median_sender_nonce = features_df.iloc[0]["median_sender_nonce"]
	contract_features.returning_user_perc = features_df.iloc[0]["returning_user_perc"]
	contract_features.n_unique_incoming_addresses = features_df.iloc[0]["n_unique_incoming_addresses"]
	contract_features.n_deployer_transactions = features_df.iloc[0]["n_deployer_transactions"]
	contract_features.contains_abi = features_df.iloc[0]["contains_abi"]

	if trust_score is not None:
		contract_features.trust_score = trust_score

	contract_features.save()
	