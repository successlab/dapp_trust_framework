from celery import shared_task

from contract_relations.link_finder import get_code_links, get_attribute_links
from contract_relations.submodels.contract_models import ContractRelation, Address
from trust_scoring.models import ContractFeatures
from utils.basic_web3.address_classifier import is_contract, is_null_address


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

	relations_stored = ContractRelation.objects.filter(parent=parent_address_obj).exists()
	if not relations_stored:
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
