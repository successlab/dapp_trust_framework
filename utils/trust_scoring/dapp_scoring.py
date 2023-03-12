from trust_scoring.models import ContractFeatures


def get_dapp_trust_score(explored_contracts, method="computation_burden"):
	"""
	Params:
		explored_contracts: A dictionary of addresses and their individual trust score
		method: The method that needs to be used to calculate the DApp trust score
			Types:
				computation_burden - Weight the contracts according to their computation burden in the process (Gas)
	"""

	dapp_trust_score = None
	if method == "computation_burden":
		computation_burdens = {}

		for address in explored_contracts.keys():
			computation_burden = ContractFeatures.objects.get(contract__address__eth_address=address).avg_gas_consumed
			computation_burdens[address] = computation_burden

		print("Computation burdens: ", computation_burdens)
		print("Individual trust scores: ", explored_contracts)

		computation_burdens_scores = {}
		for address in explored_contracts.keys():
			computation_burdens_scores[address] = explored_contracts[address] * computation_burdens[address]

		dapp_trust_score = sum(computation_burdens_scores.values())/sum(computation_burdens.values())

		print("Computation burden weighted scores: ", computation_burdens_scores)

	return dapp_trust_score
