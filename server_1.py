from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from parse import parse_goods_page, parseHandler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Good(db.Model):
    id         = db.Column(db.Integer,primary_key=True)
    title      = db.Column(db.String(120))
    link       = db.Column(db.String(120))
    category   = db.Column(db.String(120))

    def __repr__(self):
        return '{} {}'.format(self.id, self.title)

db.create_all()


@app.route('/loadData')
def loadData():
    db.drop_all()
    db.create_all()
    subCatList = []
    catalogue = parseHandler('https://leroymerlin.ru/catalogue/',
                           'div.items li',
                           'a span',
                           'a'
                           )

    for subCat in catalogue[0:1]:
        subCatList = subCatList + parseHandler(subCat['link'],
                            'div.items li',
                           'a span',
                           'a'
                           )

    for subCat in subCatList[0:1]:
        # goodList = parseHandler(subCat['link'],
        #                     'div.product-name',
        #                    'a',
        #                    'a',
        #                    )
        goodList = parse_goods_page(subCat['link'])

        for good in goodList:
            row = Good(title = good.name,
                       link = good.link,
                       category = subCat['text'])
            db.session.add(row)
            db.session.commit()

    return '''{'status': 'ok'}'''


@app.route('/')
def home():
    data = Good.query.all()
    return render_template('home.html', data=data)
