import requests


def get_github_search_results_page(contract_address, github_cookie):
    cookies = github_cookie

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "If-None-Match": 'W/"9fef31759f86dcc19c79727867089080"',
    }

    params = {
        "q": contract_address,
        "type": "code",
    }

    response = requests.get(
        "https://github.com/search", params=params, cookies=cookies, headers=headers
    )

    return response.content
