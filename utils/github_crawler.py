from django.conf import settings

from utils.statops.github_scoring import get_overall_usage_score
from utils.crawler_ops.content_ops import (
    usage_stats,
    get_max_pagecount,
    get_contract_users_and_repos,
)
from utils.crawler_ops.fetching.search_results import get_github_search_results_page

from contract_relations.models import *


def write_search_results_into_db(results, parent_contract_address):
    if len(Contract.objects.filter(address=parent_contract_address)) == 0:
        dapp = DApp()
        dapp.save()

        parent_contract = Contract()
        parent_contract.address = parent_contract_address
        parent_contract.dapp = dapp
        parent_contract.save()

    else:
        parent_contract = Contract.objects.get(address=parent_contract_address)

    for user in results.keys():
        print(user)


def get_github_search_results(contract_address):
    search_results_content = get_github_search_results_page(
        contract_address, settings.GITHUB_HEADER
    )
    lang_counts = usage_stats(search_results_content)
    print("Overall usage scoare: ", get_overall_usage_score(lang_counts))
    print(
        "Total number of pages available: ", get_max_pagecount(search_results_content)
    )
    code_search_results = get_contract_users_and_repos(search_results_content)
    print("Code search results: ", code_search_results)
    return code_search_results

def get_github_all_code_search_results(contract_address):
    search_results_content = get_github_search_results_page(
        contract_address, settings.GITHUB_HEADER
    )
    code_search_results = get_contract_users_and_repos(search_results_content)
    max_pagecount = get_max_pagecount(search_results_content)

    if max_pagecount > 1:
        page = 2

        for i in range(page, max_pagecount + 1):
            search_results_content = get_github_search_results_page(
                contract_address, settings.GITHUB_HEADER, page_number=i
            )
            code_search_results = get_contract_users_and_repos(search_results_content, code_search_results)

    for k, v in code_search_results.items():
        code_search_results[k] = list(set(v))

    return code_search_results
