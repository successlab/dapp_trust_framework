import requests


def get_github_search_results_page(contract_address, github_header, page_number=None):
    headers = github_header

    if page_number is None:
        params = {
            "q": contract_address,
            "type": "code",
        }

    else:
        params = {
            "p": page_number,
            "q": contract_address,
            "type": "code",
        }

    response = requests.get(
        "https://github.com/search", params=params, headers=headers
    )

    return response.content
