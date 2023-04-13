from contract_relations.submodels.contract_models import Contract
from utils.extractors.etherscan_extractor import get_all_contract_props
from celery import shared_task


def clean_dapp_family_links(dapp_family_links_dict, search_address):
	'''
		Response format:
		[
			{
				"contract_name": "ABC",
				"contract_address": "0x124h335huqn12",
				"trust_score": 75,
			},
			...
		]
	'''
	dapp_family_links_list = []

	for contract_address in dapp_family_links_dict.keys():
		if contract_address.lower() == search_address.lower():
			continue

		linked_dict = {
			"contract_address": contract_address,
			"trust_score": dapp_family_links_dict[contract_address],
			"contract_name": get_contarct_name(contract_address),
		}

		if contract_address.lower() != search_address.lower():
			dapp_family_links_list.append(linked_dict)

	return dapp_family_links_list


def get_contarct_name(address):
	contract_name = Contract.objects.get(address__eth_address=address).name

	if contract_name is None:
		_, _, _, contract_name = get_all_contract_props(address)

		if contract_name is None:
			contract_name = "Unknown"

		update_contract_name.delay(
			address=address,
			name=contract_name,
		)

	return contract_name


@shared_task
def update_contract_name(address, name):
	contract_obj = Contract.objects.get(address__eth_address=address)
	contract_obj.name = name
	contract_obj.save()
