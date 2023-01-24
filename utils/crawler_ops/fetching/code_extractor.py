import re

import requests

from utils.crawler_ops.content_ops import get_repo_code_links, get_max_pagecount
from utils.crawler_ops.fetching.search_results import get_repo_search_results_page


def get_all_code_files(user, repo, languages=None):
    if languages is None:
        languages = [None]

    repo_links = []

    for language in languages:
        res = get_repo_search_results_page(
            user,
            repo,
            language=language,
        )
        try:
            n_pages = get_max_pagecount(res)
        except:
            n_pages = 1

        repo_links = get_repo_code_links(res, repo_links)

        if n_pages > 1:
            for i in range(2, n_pages + 1):
                res = get_repo_search_results_page(
                    user,
                    repo,
                    language=language,
                    page_number=i
                )

                repo_links = get_repo_code_links(res, repo_links)

    return list(set(repo_links))


def clean_links(repo_code_links):
    cleaned_links = []
    for link in repo_code_links:
        cleaned_link = link.replace("blob/", "")
        cleaned_links.append(
            "https://raw.githubusercontent.com" + cleaned_link
        )

    return cleaned_links


def download_code(github_raw_code_link):
    # Send a GET request to the URL
    response = requests.get(github_raw_code_link)
    # Get the contents of the response
    content = response.text
    return content


# Check if the code is importing web3
def is_importing_web3(code):
    # Regular expression to match the import statement of web3
    pattern = r"(import|require)\s+web3"
    match = re.search(pattern, code, re.IGNORECASE)
    if match:
        return True
    else:
        # Regular expression to match the script tag containing web3.js
        pattern = r"<script[^>]*src=['\"]web3.js['\"][^>]*>"
        match = re.search(pattern, code, re.IGNORECASE)
        if match:
            return True
        else:
            return False


# Check if the code is triggering metamask
def is_using_meta_mask(code):
    # Regular expression to match the web3 code that opens up MetaMask
    pattern = r"(ethereum\.enable\(\))|(web3\.eth\.requestAccounts\()|(web3\.eth\.getAccounts\()|(web3\.eth\.getCoinbase\()"

    # Check if the code contains any of the MetaMask enable code
    match = re.search(pattern, code, re.IGNORECASE)

    if match:
        return True
    else:
        return False
