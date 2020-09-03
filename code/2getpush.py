import requests
from bs4 import BeautifulSoup


def get_all_push(url, count):
    # 建立回應
    response = requests.get(url)
    c = count
    # 印出
    # print(response.text)

    # 將原始碼做整理
    soup = BeautifulSoup(response.text, "html.parser")
    # 使用find_all()找尋特定目標
    articles = soup.find_all('div', 'push')

    # # 取得留言內容
    # for article in articles:
    #     userid = article.find(
    #         'span', 'f3 hl push-userid').getText().replace(':', '').strip()
    #     messages = article.find('span', 'f3 push-content').getText()
    #     print(userid + messages)

    # 寫入檔案中
    with open('article/fliter/iwant_push.txt', 'a') as f:
        for article in articles:
            try:
                userid = article.find(
                    'span', 'f3 hl push-userid').getText().replace(':', '').strip()
                messages = article.find('span', 'f3 push-content').getText()
                # print(userid + messages)
                print(c)
                f.write(userid + messages + "\n")
            except AttributeError:
                continue


if __name__ == "__main__":
    with open('article/fliter/iwant.txt', 'r') as fp:
        all_lines = fp.readlines()
    urls = []

    for i in all_lines:
        urls.append(i.strip("\n"))
    # print(urls)

    count = 1
    for url in range(1, len(urls), 2):
        print(count)
        get_all_push(urls[url], count)
        count += 1
