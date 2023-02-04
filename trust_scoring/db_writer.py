from web3 import Web3
from django.conf import settings
from celery import shared_task

from contract_relations.link_finder import get_code_links, get_attribute_links
from contract_relations.submodels.contract_models import ContractRelation, Address
from trust_scoring.models import ContractFeatures
from utils.basic_web3.address_classifier import is_contract, is_null_address
from utils.trust_scoring.data_persistance import write_features_df_into_db
from utils.trust_scoring.feature_extractor import get_features_df
from utils.trust_scoring.ml_model_runner import get_prob_trust_score


def generate_and_store_score(address):
	w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
	address = w3.toChecksumAddress(address)
	contract_attribs_df = get_features_df(address)

	prob_score = get_prob_trust_score(contract_attribs_df)

	write_features_df_into_db(
		address,
		contract_attribs_df,
		trust_score=prob_score,
	)

	response_dict = {
		"trust_score": prob_score,
		"contract_attributes": contract_attribs_df.iloc[0].to_dict(),
	}

	code_contracts = find_links_and_store_in_db(address)
	response_dict["links"] = code_contracts

	return response_dict


def find_links_and_store_in_db(address):
	code_links = get_code_links(address)
	attribute_links = get_attribute_links(address)

	code_contracts = []
	for link_address in code_links:
		if is_contract(link_address):
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

	# Cleaning the linked addresses
	for i in range(len(code_links)):
		code_links[i] = w3.toChecksumAddress(code_links[i])

	for i in range(len(attribute_links)):
		attribute_links[i] = w3.toChecksumAddress(attribute_links[i])

	address_type = "NullContract" if is_null_address(address) else ""
	if address_type == "":
		address_type = "Contract" if is_contract(address) else "EOA"

	parent_address_obj = Address.objects.get_or_create(
		eth_address=address,
		type=address_type,
	)
	parent_address_obj[0].save()

	if address_type == "NullContract":
		return

	for link in code_links:
		child_address_obj = Address.objects.get_or_create(
			eth_address=link
		)
		child_address_obj[0].save()

		cr = ContractRelation.objects.get_or_create(
			parent=parent_address_obj[0],
			child=child_address_obj[0],
			relation_type="CodeMention"
		)
		cr[0].save()

	for link in attribute_links:
		child_address_obj = Address.objects.get_or_create(
			eth_address=link
		)
		child_address_obj[0].save()

		cr = ContractRelation.objects.get_or_create(
			parent=parent_address_obj[0],
			child=child_address_obj[0],
			relation_type="AttribVal"
		)
		cr[0].save()

	all_addresses = code_links + attribute_links
	for address in all_addresses:
		if not (is_null_address(address)) and is_contract(address):
			generate_scores(address)


@shared_task
def generate_scores(address):
	print("Generating scores for address: ", address)
	generate_and_store_score(address)
