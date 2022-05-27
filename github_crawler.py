import sys

from secrets.cookies import github_cookie
from pageops.content_ops import get_github_search_results_page, usage_stats, get_max_pagecount


def get_overall_usage_score(lang_counts):
    return sum(lang_counts.values())


if __name__ == '__main__':
    contract_address = sys.argv[1]

    search_results_content = get_github_search_results_page(contract_address, github_cookie)
    lang_counts = usage_stats(search_results_content)
    print("Overall usage scoare: ", get_overall_usage_score(lang_counts))
    print("Total number of pages available: ", get_max_pagecount(search_results_content))
