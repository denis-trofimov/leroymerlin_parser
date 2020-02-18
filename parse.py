from collections import namedtuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parseHandler(url, listSelector, textSelector, linkSelector, main_price=None):

    result = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.select(listSelector)
    unreadCnt = 0
    for card in cards:

        try:
            _dict = {}
            _dict['text'] = card.select_one(textSelector).text
            _dict['link'] =urljoin(url, card.select_one(linkSelector).get('href'))
            print(_dict['text'], _dict['link'])
            if main_price:
                print(card.select_one(main_price).get('content'))
                # _dict['main_price'] = card.select_one(main_price).get('content')

            result.append(_dict)
        except Exception as e:
            unreadCnt += 1
            print(e)



    print('unread {} rows'.format(unreadCnt))
    return result

# EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')
Good = namedtuple("Good", ('name', 'link', 'price'))

def parse_goods_page(url):
    "parse_goods_page is a new custom goods page parser"

    goods = []
    unreadCnt = 0

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.select('div.ui-sorting-cards')

    for card in cards:
        """
        <div class="ui-product-card" comparison-checked="false" shopping-list-checked="false" data-product-web-saleable="true" data-product-url="/product/shtukaturka-gipsovaya-knauf-rotband-30-kg-10073940/" data-product-category-id="shtukaturki-201709_Opus_Family" data-product-price="421.00" data-sub-category-id="20" data-category-id="65" data-product-material="Гипс" data-product-gamma="A" data-unit="NIU" data-division-id="1" data-source="Step" data-product-color="Серый" data-product-stock-value="1175" data-product-has-linked-how-tos="0" data-product-location="Catalog" data-product-id="10073940" data-product-dimension65="STD" data-product-weight="30" data-rel="js-cat-product-item" data-product-brand="KNAUF" data-place="plp" data-element-id="ui-product-card" data-ga-root="data-ga-root" data-sub-division-id="110" data-product-name="Штукатурка гипсовая Knauf Ротбанд 30 кг" shop-cart-checked="false">
        """
        good = card.select_one('div.ui-product-card')
        name = good.get('data-product-name')
        link = good.get('data-product-url')
        link = urljoin(url, link)
        price = good.get('data-product-price')
        print(name, price, link)

        goods.append(Good(name=name, link=link, price=price))

    print('unread {} rows'.format(unreadCnt))
    return goods
