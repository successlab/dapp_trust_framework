import concurrent.futures

from django.conf import settings

# from contract_relations.models import *
from utils.crawler_ops.content_ops import (
    usage_stats,
    get_max_pagecount,
    get_contract_users_and_repos,
)
from utils.crawler_ops.fetching.code_extractor import get_all_code_files, clean_links, download_code, is_importing_web3, \
    is_using_meta_mask
from utils.crawler_ops.fetching.search_results import get_github_search_results_page
from utils.statops.github_scoring import get_overall_usage_score


# def write_search_results_into_db(results, parent_contract_address):
#     if len(Contract.objects.filter(address__eth_address=parent_contract_address)) == 0:
#         dapp = DApp()
#         dapp.save()
#
#         parent_contract = Contract()
#         parent_contract.address = parent_contract_address
#         parent_contract.dapp = dapp
#         parent_contract.save()
#
#     else:
#         parent_contract = Contract.objects.get(address=parent_contract_address)
#
#     for user in results.keys():
#         print(user)


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


def check_web3js_usage(code_search_results):
    web3js_uses = []
    '''
    format:
    [
        {
            user:
            repo:
            link:
            web3js_import: True/False
            metamask_trigger: True/False
        }
    ]
    '''
    found_web3js_import = False
    found_metamask_trigger = False

    for k, v in code_search_results.items():
        user = k
        for repo in v:
            code_files = get_all_code_files(
                user,
                repo,
                languages=["JavaScript", "TypeScript"]
            )
            links = clean_links(code_files)

            for link in links:
                code = download_code(link)
                web3_import = is_importing_web3(code)
                metamask_trigger = is_using_meta_mask(code)

                if web3_import != False or metamask_trigger != False:
                    web3js_uses.append(
                        {
                            "user": user,
                            "repo": repo,
                            "link": link,
                            "web3js_import": web3_import,
                            "metamask_trigger": metamask_trigger,
                        }
                    )

                    if web3_import:
                        found_web3js_import = True

                    if metamask_trigger:
                        found_metamask_trigger = True

                    # TODO: For testing only, delete this later
                    if found_web3js_import == True and found_metamask_trigger == True:
                        return found_web3js_import, found_metamask_trigger, web3js_uses

    return found_web3js_import, found_metamask_trigger, web3js_uses


def check_web3js_usage_parallel(code_search_results):
    web3js_uses = []
    '''
    format:
    [
        {
            user:
            repo:
            link:
            web3js_import: True/False
            metamask_trigger: True/False
        }
    ]
    '''
    found_web3js_import = False
    found_metamask_trigger = False

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_link = {executor.submit(process_link, k, repo, link): (k, repo, link) for k, v in
                          code_search_results.items() for repo in v for link in
                          clean_links(get_all_code_files(k, repo, languages=["JavaScript", "TypeScript"]))}
        for future in concurrent.futures.as_completed(future_to_link):
            user, repo, link = future_to_link[future]
            try:
                web3_import, metamask_trigger = future.result()
                if web3_import != False or metamask_trigger != False:
                    web3js_uses.append(
                        {
                            "user": user,
                            "repo": repo,
                            "link": link,
                            "web3js_import": web3_import,
                            "metamask_trigger": metamask_trigger,
                        }
                    )

                    if web3_import:
                        found_web3js_import = True

                    if metamask_trigger:
                        found_metamask_trigger = True
            except Exception as e:
                print(f'{link} generated an exception: {e}')

    return found_web3js_import, found_metamask_trigger, web3js_uses


def process_link(user, repo, link):
    code = download_code(link)
    web3_import = is_importing_web3(code)
    metamask_trigger = is_using_meta_mask(code)
    return web3_import, metamask_trigger
