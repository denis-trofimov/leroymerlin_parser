from flask import Flask, render_template
from webapp.parse import parse_handler, parse_sub_category_page
from webapp.model import db, Product


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    @app.route('/parse')
    def load_data():

        sub_categories = []
        catalogue = parse_handler('https://leroymerlin.ru/catalogue/',
                                  'div.items li',
                                  'a span',
                                  'a'
                                  )

        for sub_category in catalogue[0:6]:
            sub_categories = sub_categories + parse_handler(sub_category['link'],
                                                            'div.items li',
                                                            'a span',
                                                            'a'
                                                            )

        for sub_category in sub_categories[0:6]:
            goods = parse_sub_category_page(sub_category['link'])

            for good in goods:
                row = Product(name=good.name, url=good.url, price=good.price,
                              weight=good.weight, stock=good.stock, id=good.id,
                              brand=good.brand, category=sub_category['text']
                              )
                db.session.add(row)
                db.session.commit()

        return '''{'status': 'ok'}'''

    @app.route('/')
    def home():
        data = Product.query.all()
        return render_template('home.html', data=data)

    return app
