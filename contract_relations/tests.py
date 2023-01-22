from django.test import TestCase
from utils.github_crawler import get_github_search_results, get_github_all_code_search_results
from utils.crawler_ops.fetching.search_results import get_repo_search_results_page
from utils.crawler_ops.content_ops import get_max_pagecount, get_repo_code_links

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
        res = get_repo_search_results_page(
            "surajsjain",
            "cryptopay-web",
            language="Python",
        )
        get_repo_code_links(res)
