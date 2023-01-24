from django.test import TestCase

from utils.etherscan_utils import fetch_abi
from utils.github_crawler import get_github_all_code_search_results, check_web3js_usage_parallel


class TestUtils(TestCase):
    def test_abi_fetcher(self):
        contract_address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
        print(fetch_abi(contract_address))

    def test_webjs_code_existance_check(self):
        search_address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
        res = get_github_all_code_search_results(search_address)

        found_web3js_import, found_metamask_trigger, web3js_uses = check_web3js_usage_parallel(res)
        print("found_web3js_import: ", found_web3js_import)
        print("found_metamask_trigger: ", found_metamask_trigger)
        print("web3js_uses: ", web3js_uses)


class TestAPIs(TestCase):
    pass