import requests


def get_github_search_results_page(contract_address, github_header):
    headers = github_header
    params = {
        "q": contract_address,
        "type": "code",
    }
    response = requests.get(
        "https://github.com/search", params=params, headers=headers
    )

    return response.content
