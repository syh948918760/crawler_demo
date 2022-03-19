import requests
from scrapy import Selector
import re


def get_url(keyword='medical+system', page_num=2):
    urls = []
    for p in range(page_num):
        url = 'https://link.springer.com/search/page/{}?facet-content-type=%22Article%22&query={}'.format(
            str(p), keyword)
        r = requests.get(url)
        if r.status_code != 200:
            print("Connection error: {}".format(url))
            return "", ""
        selector = Selector(text=r.text)
        dummy_urls = [re.findall('^/article.*', item) for item in selector.css('div.actions|a::attr(href)').extract()]
        urls += ['https://link.springer.com' + item[0] for item in dummy_urls if item]
    return urls


def get_keywords_abstract(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Connection error: {}".format(url))
        return "", ""
    selector = Selector(text=r.text)
    dummy_keywords = [item.extract() for item in selector.css('.c-article-subject-list__subject')]
    keywords = [re.findall(r'<li class="c-article-subject-list__subject"><span>(.+?)</span></li>', str)[0] for str in
                dummy_keywords]
    return keywords


if __name__ == '__main__':
    with open('url.txt', 'w') as f:
        urls = get_url(page_num=3)
        for url in urls:
            if url.find('fulltext.html') == -1:
                f.write(url + '\n')

    keywords = []
    with open('url.txt', 'r') as f:
        for line in f.readlines():
            url = line[:-1]
            keywords = get_keywords_abstract(url)
            print(url, keywords)
    print(keywords)
