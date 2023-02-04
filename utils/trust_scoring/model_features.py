features_and_pandas_dtypes = {
	'n_transactions': 'int',
	'avg_trx_freq': 'float',
	'avg_gas_price': 'float',
	'avg_gas_consumed': 'float',
	'median_sender_nonce': 'float',
	'returning_user_perc': 'float',
	'n_unique_incoming_addresses': 'int',
	'n_deployer_transactions': 'int',
	'contains_abi': 'int',  # Bool, but convert it into 0/1 (1 - True; 0 - False)
}

feature_weightages = {
	'n_transactions': 0.08025426959845469,
	'avg_trx_freq': 0.0759721055795251,
	'avg_gas_price': 0.24122253410988187,
	'avg_gas_consumed': 0.12663152183848098,
	'median_sender_nonce': 0.17753834793346077,
	'returning_user_perc': 0.03689057281240384,
	'n_unique_incoming_addresses': 0.06706199090260874,
	'n_deployer_transactions': 0.043608406586295174,
	'contains_abi': 0.1508202506388889
}
