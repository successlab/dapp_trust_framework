from web3 import Web3
from django.conf import settings
from celery import shared_task

from contract_relations.submodels.contract_models import ContractRelation, Address
from trust_scoring.models import ContractFeatures
from utils.basic_web3.address_classifier import is_contract, is_null_address
from utils.extractors.etherscan_extractor import get_all_contract_props
from utils.trust_scoring.contract_links import get_linked_addresses
from utils.trust_scoring.dapp_scoring import get_dapp_trust_score
from utils.trust_scoring.data_persistance import write_features_df_into_db
from utils.trust_scoring.feature_extractor import get_features_df
from utils.trust_scoring.ml_model_runner import get_prob_trust_score
from utils.trust_scoring.model_features import legit_limits, malicious_limits


def generate_and_store_score(address):
	w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
	address = w3.toChecksumAddress(address.lower())
	contract_attribs_df, web3js_uses, prob_score = get_features_df(address)

	_, _, is_proxy, contract_name = get_all_contract_props(address)

	if prob_score is None:
		prob_score = get_prob_trust_score(contract_attribs_df)
		write_features_df_into_db.delay(
			address=address,
			features_df_json=contract_attribs_df.to_json(),
			is_proxy=is_proxy,
			contract_name=contract_name,
			web3js_uses_dict=web3js_uses,
			trust_score=prob_score,
		)

	response_dict = {
		"contract_trust_score": prob_score,
		"contract_name": contract_name,
		"is_proxy": is_proxy,
	}

	dapp_family_links, dapp_trust_score = get_collective_linked_score_bfs(address)
	if dapp_family_links is None:
		dapp_family_links = "Generating, check back later"
		dapp_trust_score = "Generating, check back later"

	response_dict["dapp_trust_score"] = dapp_trust_score
	response_dict["contract_attributes"] = contract_attribs_df.iloc[0].to_dict()
	code_contracts = find_links_and_store_in_db(address)
	response_dict["immediate_links"] = code_contracts
	response_dict["dapp_family_links"] = dapp_family_links
	response_dict["open_source_web3js_interfaces"] = web3js_uses

	response_dict["limits"] = {}
	response_dict["limits"]["legit_limits"] = legit_limits
	response_dict["limits"]["malicious_limits"] = malicious_limits

	return response_dict


def find_links_and_store_in_db(address):
	w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))

	code_links, attribute_links = get_linked_addresses(address)

	code_contracts = []
	for link_address in code_links:
		if is_contract(link_address) and not(is_null_address(link_address)):
			link_dict = {"address": link_address}

			try:
				score = ContractFeatures.objects.get(contract__address__eth_address=link_address).trust_score
			except:
				score = "Not available, check back later"

			link_dict["trust_score"] = score

			code_contracts.append(link_dict)

	process_db_store.delay(address, code_links, attribute_links)
	return code_contracts


@shared_task
def process_db_store(address, code_links, attribute_links):
	w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))

	print("Processing DB store for address: ", address)
	if ContractRelation.objects.filter(parent__contract__address__eth_address=address).exists():
		return

	# Cleaning the linked addresses
	# for i in range(len(code_links)):
	# 	code_links[i] = w3.toChecksumAddress(code_links[i].lower())
	#
	# for i in range(len(attribute_links)):
	# 	attribute_links[i] = w3.toChecksumAddress(attribute_links[i].lower())

	address_type = "NullContract" if is_null_address(address) else ""
	if address_type == "":
		address_type = "Contract" if is_contract(address) else "EOA"

	parent_address_obj = Address.objects.get_or_create(
		eth_address=address,
		type=address_type,
	)

	if address_type == "NullContract":
		return

	for link in code_links:
		child_address_obj = Address.objects.get_or_create(
			eth_address=link
		)

		cr = ContractRelation.objects.get_or_create(
			parent=parent_address_obj[0],
			child=child_address_obj[0],
			relation_type="CodeMention"
		)

	for link in attribute_links:
		child_address_obj = Address.objects.get_or_create(
			eth_address=link
		)

		cr = ContractRelation.objects.get_or_create(
			parent=parent_address_obj[0],
			child=child_address_obj[0],
			relation_type="AttribVal"
		)

	all_addresses = code_links + attribute_links
	for address in all_addresses:
		if not (is_null_address(address)) and is_contract(address) and \
				not(ContractFeatures.objects.filter(contract__address__eth_address=address).exists()):
			generate_scores.delay(address)


@shared_task
def generate_scores(address):
	print("Generating scores for address: ", address)
	generate_and_store_score(address)


def get_collective_linked_score_bfs(address):
	all_contracts = [address]

	explored = {}
	scores_to_generate = []

	# Running BFS and exploring deep links
	while len(all_contracts) > 0:
		contract_address_in_focus = all_contracts.pop()

		if not(ContractFeatures.objects.filter(contract__address__eth_address=contract_address_in_focus).exists()):
			scores_to_generate.append(contract_address_in_focus)
			continue

		else:
			trust_score = ContractFeatures.objects.get(
				contract__address__eth_address=contract_address_in_focus
			).trust_score
			explored[contract_address_in_focus] = trust_score

			code_links, _ = get_linked_addresses(contract_address_in_focus, False)

			for link in code_links:
				if (link not in explored) and is_contract(link) and (is_null_address(link) is False):
					all_contracts = [link] + all_contracts

	# Filling in the missing contract scores
	if len(scores_to_generate) != 0:
		for contract_address in scores_to_generate:
			generate_scores.delay(contract_address)

		return None, -1

	# Calculating the overall trust score
	# dapp_trust_score = sum(explored.values())/len(explored)
	dapp_trust_score = get_dapp_trust_score(explored)
	return explored, dapp_trust_score
