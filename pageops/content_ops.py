from bs4 import BeautifulSoup


def usage_stats(search_results_content):
    response_soup = BeautifulSoup(search_results_content, 'html.parser')

    languages_and_counts_raw = response_soup.find("div", class_="border rounded-2 p-3 mb-3 d-none d-md-block") \
        .find_all("a", class_="filter-item")

    lang_counts = {}

    for raw_ele in languages_and_counts_raw:
        content_eles = raw_ele.text.split()
        lang_name = ''.join(content_eles[1:])
        lang_files_count = int(content_eles[0])
        lang_counts[lang_name] = lang_files_count

    return lang_counts


def get_max_pagecount(search_results_content):
    response_soup = BeautifulSoup(search_results_content, 'html.parser')
    paginator = response_soup.find("div", class_="paginate-container codesearch-pagination-container")
    return int(paginator.find_all("a")[-2].text)