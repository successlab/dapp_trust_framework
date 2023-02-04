from contract_relations.link_finder import get_code_links, get_attribute_links
from contract_relations.submodels.contract_models import ContractRelation, Address
from trust_scoring.models import ContractFeatures
from utils.basic_web3.address_classifier import is_contract


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

	# TODO: Push everything from this to the next TODO to Celery

	parent_address_obj = Address.objects.get_or_create(
		eth_address=address
	)
	parent_address_obj[0].save()

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

	# TODO: generate trust scores for the linked contracts that don't already have one

	return code_contracts
