from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    brand = db.Column(db.String(30))
    url = db.Column(db.String(200))
    category = db.Column(db.String(100))
    price = db.Column(db.String(10))
    weight = db.Column(db.Float)
    stock = db.Column(db.Integer)

    def __repr__(self):
        return '{} {}'.format(self.id, self.title)
