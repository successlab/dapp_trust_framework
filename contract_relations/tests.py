from django.test import TestCase
from utils.github_crawler import get_github_search_results, write_search_results_into_db

# Create your tests here.
class TestGithubSearch(TestCase):
    def test_search(self):
        search_address = "0xe34139463bA50bD61336E0c446Bd8C0867c6fE65"
        res = get_github_search_results(search_address)
        write_search_results_into_db(res, search_address)
