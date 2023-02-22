from django.test import TestCase

# Create your tests here.
from trust_scoring.models import ContractFeatures
from utils.trust_scoring.data_persistance import write_features_df_into_db
from utils.trust_scoring.feature_extractor import get_features_df
from utils.trust_scoring.ml_model_runner import get_prob_trust_score


class TestUtils(TestCase):
	def test_feature_loading(self):
		address = "0x386F6F20BC8f3FF753fE6B731FD93fF8a0bA18e4"
		contract_attribs_df, _, _ = get_features_df(address)

		self.assertNotEqual(len(contract_attribs_df), 0)

	def test_prob_scoring(self):
		# AAVE Liquidate
		address = "0x386F6F20BC8f3FF753fE6B731FD93fF8a0bA18e4"
		contract_attribs_df, _, _ = get_features_df(address)

		prob_score = get_prob_trust_score(contract_attribs_df)
		print(prob_score)

	def test_write_features_df_into_db(self):
		# AAVE Liquidate
		address = "0x386F6F20BC8f3FF753fE6B731FD93fF8a0bA18e4"
		contract_attribs_df, _, _ = get_features_df(address)

		prob_score = get_prob_trust_score(contract_attribs_df)

		write_features_df_into_db(
			address,
			contract_attribs_df,
			trust_score=prob_score,
		)

		contract_features = ContractFeatures.objects.filter(contract__address__eth_address=address)

		self.assertGreater(len(contract_features), 0)
