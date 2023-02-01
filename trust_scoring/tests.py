from django.test import TestCase

# Create your tests here.
from utils.trust_scoring.feature_extractor import get_features_df
from utils.trust_scoring.ml_model_runner import get_prob_trust_score


class TestUtils(TestCase):
	def test_feature_loading(self):
		address = "0x386F6F20BC8f3FF753fE6B731FD93fF8a0bA18e4"
		contract_attribs_df = get_features_df(address)

		self.assertNotEqual(len(contract_attribs_df), 0)

	def test_prob_scoring(self):
		# AAVE Liquidate
		address = "0x386F6F20BC8f3FF753fE6B731FD93fF8a0bA18e4"
		contract_attribs_df = get_features_df(address)

		prob_score = get_prob_trust_score(contract_attribs_df)
		print(prob_score)
