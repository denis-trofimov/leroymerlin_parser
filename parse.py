import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parseHandler(url, listSelector, textSelector, linkSelector, main_price=None):

    result = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.select(listSelector)
    unreadCnt = 0
    for elem in cards:

        try:
            _dict = {}
            _dict['text'] = elem.select_one(textSelector).text
            _dict['link'] =urljoin(url, elem.select_one(linkSelector).get('href'))
            print(_dict['text'], _dict['link'])
            if main_price:
                print(elem.select_one(main_price).get('content'))
                # _dict['main_price'] = elem.select_one(main_price).get('content')

            result.append(_dict)
        except Exception as e:
            unreadCnt += 1
            print(e)



    print('unread {} rows'.format(unreadCnt))
    return result

def parse_goods_page(url):
    "parse_goods_page is a new custom goods page parser"
    listSelector = 'div.product-name'
    linkSelector = 'a'
    textSelector = 'a'

    result = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.select(listSelector)
    unreadCnt = 0
    for elem in cards:
        try:
            _dict = {}
            _dict['text'] = elem.select_one(textSelector).text
            _dict['link'] =urljoin(url, elem.select_one(linkSelector).get('href'))
            print(_dict['text'], _dict['link'])
            # if main_price:
            #     print(elem.select_one(main_price).get('content'))
                # _dict['main_price'] = elem.select_one(main_price).get('content')

            result.append(_dict)
        except Exception as e:
            unreadCnt += 1
            print(e)

    print('unread {} rows'.format(unreadCnt))
    return result
