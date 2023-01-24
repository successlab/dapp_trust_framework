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


def get_repo_search_results_page(user, repo, language=None, page_number=None):
    params = {}

    if language is not None:
        params["l"] = language
    if page_number is not None:
        params["p"] = page_number

    url = f"https://github.com/{user}/{repo}/"
    if len(params) != 0:
        url += "search?"

    for k, v in params.items():
        url += k + "=" + str(v) + "&"

    response = requests.get(url)

    return response.content
