features_and_pandas_dtypes = {
	# 'n_transactions': 'int',
	'avg_trx_freq': 'float',
	'avg_gas_price': 'float',
	'avg_gas_consumed': 'float',
	'median_sender_nonce': 'float',
	'returning_user_perc': 'float',
	'n_unique_incoming_addresses': 'int',
	'n_deployer_transactions': 'int',
	'contains_abi': 'int',  # Bool, but convert it into 0/1 (1 - True; 0 - False)
	'contains_w3_js': 'int',  # Bool, but convert it into 0/1 (1 - True; 0 - False)
}

feature_weightages = {
	'avg_trx_freq': 8.64769820082531,
	'avg_gas_price': 17.212321412386647,
	'avg_gas_consumed': 11.010181668459143,
	'median_sender_nonce': 11.466813221967087,
	'returning_user_perc': 5.163604743908352,
	'n_unique_incoming_addresses': 7.951081099086453,
	'n_deployer_transactions': 5.032960947712193,
	'contains_abi': 29.383812279865477,
	'contains_w3_js': 4.131526425789332
}
