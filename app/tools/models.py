from . import db


class AppTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Template('{self.name}', '{self.url}')"
