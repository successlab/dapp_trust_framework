from bs4 import BeautifulSoup


def usage_stats(search_results_content):
    response_soup = BeautifulSoup(search_results_content, "html.parser")

    languages_and_counts_raw = response_soup.find(
        "div", class_="border rounded-2 p-3 mb-3 d-none d-md-block"
    ).find_all("a", class_="filter-item")

    lang_counts = {}

    for raw_ele in languages_and_counts_raw:
        try:
            content_eles = raw_ele.text.split()
            lang_name = "".join(content_eles[1:])
            lang_files_count = int(content_eles[0])
            lang_counts[lang_name] = lang_files_count
        except:
            pass

    return lang_counts


def get_max_pagecount(search_results_content):
    response_soup = BeautifulSoup(search_results_content, "html.parser")
    paginator = response_soup.find(
        "div", class_="paginate-container codesearch-pagination-container"
    )
    try:
        return int(paginator.find_all("a")[-2].text)
    except:
        return 1


def get_contract_users_and_repos(search_results_content, users_and_repos_mapping=None):
    if users_and_repos_mapping is None:
        users_and_repos_mapping = {}
    response_soup = BeautifulSoup(search_results_content, "html.parser")

    code_search_results = response_soup.find(
        "div", class_="col-12 col-md-9 float-left px-2 pt-3 pt-md-0 codesearch-results"
    )
    try:
        users_and_repos_raw = code_search_results.find_all("a", class_="Link--secondary")

        for user_and_repo in users_and_repos_raw:
            user, repo = user_and_repo.text.split("/")
            user = user.strip()
            repo = repo.strip()
            if user in users_and_repos_mapping:
                users_and_repos_mapping[user].append(repo)
            else:
                users_and_repos_mapping[user] = [repo]

    except:
        pass

    return users_and_repos_mapping


def get_repo_code_links(search_results_content, code_links=None):
    if code_links is None:
        code_links = []

    response_soup = BeautifulSoup(search_results_content, "html.parser")
    search_results = response_soup.find(
        "div", class_="code-list"
    )

    try:
        link_elements = search_results.find_all("a")

        for link_element in link_elements:
            code_links.append(link_element.get('href'))

        return code_links

    except Exception:
        return []
