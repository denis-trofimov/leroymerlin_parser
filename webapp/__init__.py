from flask import Flask, render_template
from webapp.parse import parse_handler, parse_sub_category_page
from flask_sqlalchemy import SQLAlchemy


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    url = db.Column(db.String(120))
    category = db.Column(db.String(120))

    def __repr__(self):
        return '{} {}'.format(self.id, self.title)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db = SQLAlchemy(app)

    @app.route('/parse')
    def load_data():
        db.drop_all()
        db.create_all()
        sub_categories = []
        catalogue = parse_handler('https://leroymerlin.ru/catalogue/',
                                  'div.items li',
                                  'a span',
                                  'a'
                                  )

        for sub_category in catalogue[0:1]:
            sub_categories = sub_categories + parse_handler(sub_category['link'],
                                                            'div.items li',
                                                            'a span',
                                                            'a'
                                                            )

        for sub_category in sub_categories[0:1]:
            goods = parse_sub_category_page(sub_category['link'])

            for good in goods:
                row = Good(title=good.name,
                           url=good.url,
                           category=sub_category['text'])
                db.session.add(row)
                db.session.commit()

        return '''{'status': 'ok'}'''

    @app.route('/')
    def home():
        data = Good.query.all()
        return render_template('home.html', data=data)

    return app
