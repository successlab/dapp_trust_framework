from web3 import Web3
from django.conf import settings

from contract_relations.link_finder import get_code_links, get_attribute_links


def get_linked_addresses(address, check_attribute_links=True):
	w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))

	code_links = get_code_links(address)

	# Cleaning the links
	for i in range(len(code_links)):
		code_links[i] = w3.toChecksumAddress(code_links[i].lower())

	if check_attribute_links is True:
		attribute_links = get_attribute_links(address)

		# Cleaning the links
		for i in range(len(attribute_links)):
			attribute_links[i] = w3.toChecksumAddress(attribute_links[i].lower())

	else:
		attribute_links = None

	return code_links, attribute_links
