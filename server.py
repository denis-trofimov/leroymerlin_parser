from flask import Flask, render_template
from parse import parse_handler, parse_goods_page
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    link = db.Column(db.String(120))
    category = db.Column(db.String(120))

    def __repr__(self):
        return '{} {}'.format(self.id, self.title)


@app.route('/parse')
def load_data():
    # db.drop_all()
    # db.create_all()
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
        goods = parse_goods_page(sub_category['link'])

        for good in goods:
            row = Good(title=good.name,
                       link=good.link,
                       category=sub_category['text'])
            db.session.add(row)
            db.session.commit()

    return '''{'status': 'ok'}'''


@app.route('/')
def home():
    data = Good.query.all()
    return render_template('home.html', data=data)
