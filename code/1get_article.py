import requests
from bs4 import BeautifulSoup


def get_all_href(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.title")
    for item in results:
        a_item = item.select_one("a")
        if a_item:
            a_item = 'https://www.ptt.cc' + a_item.get('href')
            article_href.append(item.text)
            article_href.append(a_item)


if __name__ == "__main__":

    article_href = []
    # title = []
    pages = 293

    for page in range(1, pages+1):
        print(page)
        url = "https://www.ptt.cc/bbs/MobileComm/search?page=" + \
            str(page)+"&q=recommend%3A50"
        get_all_href(url=url)
    # print(article_href)
    print("Finish")

    with open('article_site50.txt', 'w') as f:
        for article in article_href:
            f.write(article)
