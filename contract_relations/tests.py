from django.test import TestCase

from utils.github_crawler import get_github_search_results, get_github_all_code_search_results, \
    check_web3js_usage_parallel


# Create your tests here.
class TestGithubSearch(TestCase):
    def test_one_page_search(self):
        # pass
        search_address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
        res = get_github_search_results(search_address)
        print(res)
        # write_search_results_into_db(res, search_address)

    def test_all_page_search(self):
        search_address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
        res = get_github_all_code_search_results(search_address)
        print(res)

    def test_code_fetching(self):
        search_address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
        res = get_github_all_code_search_results(search_address)

        found_web3js_import, found_metamask_trigger, web3js_uses = check_web3js_usage_parallel(res)
        print("found_web3js_import: ", found_web3js_import)
        print("found_metamask_trigger: ", found_metamask_trigger)
        print("web3js_uses: ", web3js_uses)
