from django.test import TestCase

# Create your tests here.
from utils.trust_scoring.feature_extractor import get_features_df


class TestUtils(TestCase):
	def test_feature_loading(self):
		address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
		contract_attribs_df = get_features_df(address)

		print(contract_attribs_df)
