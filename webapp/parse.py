import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import namedtuple


"A new custom products tuple"
Product = namedtuple("Product", ('id', 'name', 'brand', 'url', 'price', 'weight', 'stock'))


def parse_handler(url, listSelector, textSelector, linkSelector):

    result = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.select(listSelector)
    unread_count = 0
    for card in cards:

        try:
            _dict = {}
            _dict['text'] = card.select_one(textSelector).text
            _dict['link'] = urljoin(
                url, card.select_one(linkSelector).get('href'))
            print(_dict['text'], _dict['link'])
            result.append(_dict)
        except Exception as e:
            unread_count += 1
            print(e)

    print('unread {} rows'.format(unread_count))
    return result


def parse_sub_category_page(url):
    "parse_goods_page is a new custom goods page parser"
    responce = requests.get(url)
    if not responce.ok:
        return []

    return parse_products_cards(responce.content, url)


def parse_products_cards(content, baseurl):
    """Parse product cards

    <div class="ui-product-card" comparison-checked="false" 
    shopping-list-checked="false" data-product-web-saleable="true" 
    data-product-url="/product/shtukaturka-gipsovaya-knauf-rotband-30-kg-10073940/" 
    data-product-category-id="shtukaturki-201709_Opus_Family" 
    data-product-price="418.00" data-sub-category-id="20" data-category-id="65" 
    data-product-material="Гипс" data-product-gamma="A" data-unit="NIU" 
    data-division-id="1" data-source="Step" data-product-color="Серый" 
    data-product-stock-value="1196" data-product-has-linked-how-tos="0" 
    data-product-location="Catalog" data-product-id="10073940" 
    data-product-dimension65="STD" data-product-weight="30" 
    data-rel="js-cat-product-item" data-product-brand="KNAUF" data-place="plp" 
    data-element-id="ui-product-card" data-ga-root="data-ga-root" 
    data-sub-division-id="110" 
    data-product-name="Штукатурка гипсовая Knauf Ротбанд 30 кг">
    """
    products = []
    unread_count = 0
    soup = BeautifulSoup(content, 'html.parser')
    cards = soup.select('div.ui-sorting-cards')

    for card in cards:
        product = card.select_one('div.ui-product-card')
        name = product.get('data-product-name')
        url = product.get('data-product-url')
        url = urljoin(baseurl, url)
        price = product.get('data-product-price')
        # print(name, price, url)
        weight = float(product.get('data-product-weight'))
        id = int(product.get('data-product-id'))
        stock = int(product.get('data-product-stock-value'))
        brand = product.get('data-product-brand')
        new_product = Product(name=name, url=url, price=price, weight=weight, 
            stock=stock, id=id, brand=brand)
        products.append(new_product)

    print('unread {} rows'.format(unread_count))
    return products
