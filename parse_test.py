from parse import parse_products_cards
import pytest


@pytest.fixture
def sub_category_content():
    with open("tests/leroymerlin.ru_catalogue_shtukaturki.html", "rb") as file:
        content = file.read()
    return content


def test_parse_products_page(sub_category_content, url="https://leroymerlin.ru/catalogue/shtukaturki/"):
    """
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
    products = parse_products_cards(sub_category_content, url)
    product = products[0]
    assert product.name == "Штукатурка гипсовая Knauf Ротбанд 30 кг"
    assert product.price == "418.00"
    assert product.weight == 30
    assert product.id == 10073940
    assert product.stock == 1196
    assert product.category == "shtukaturki-201709_Opus_Family"
    assert product.sub_category_id == 20
    assert product.category_id == 65
    assert product.web_saleable == "true"
    assert product.material == "Гипс"
    assert product.gamma == "A"
    assert product.color == "Серый"
    assert product.brand == "KNAUF"
