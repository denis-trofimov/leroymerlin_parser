from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    url = db.Column(db.String(120))
    category = db.Column(db.String(120))

    def __repr__(self):
        return '{} {}'.format(self.id, self.title)
