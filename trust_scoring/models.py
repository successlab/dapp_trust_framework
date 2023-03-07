from datetime import timedelta

from django.db import models
from contract_relations.models import Contract


# Create your models here.
class ContractFeatures(models.Model):
	contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

	# Transaction-based features
	term_length = models.DurationField(default=timedelta(days=183))
	# n_transactions = models.IntegerField()
	avg_trx_freq = models.FloatField()
	avg_gas_price = models.FloatField(default=None, null=True)
	avg_gas_consumed = models.FloatField()
	median_sender_nonce = models.FloatField()
	returning_user_perc = models.FloatField()
	n_unique_incoming_addresses = models.IntegerField()

	# Owner-based features
	n_deployer_transactions = models.IntegerField()
	contains_abi = models.BooleanField()

	# Web3js-based features
	web3js_uses = models.JSONField(default=None, null=True)

	# Model predicted score
	trust_score = models.IntegerField(null=True, default=None)
	