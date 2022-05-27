import sys

from secrets.cookies import github_cookie

from statops.github_scoring import get_overall_usage_score
from pageops.content_ops import usage_stats, get_max_pagecount
from pageops.fetching.search_results import get_github_search_results_page


if __name__ == '__main__':
    contract_address = sys.argv[1]

    search_results_content = get_github_search_results_page(contract_address, github_cookie)
    lang_counts = usage_stats(search_results_content)
    print("Overall usage scoare: ", get_overall_usage_score(lang_counts))
    print("Total number of pages available: ", get_max_pagecount(search_results_content))
