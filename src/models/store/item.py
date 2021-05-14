from db import db
from datetime import datetime
from typing import List


class ItemModel(db.Model):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    image = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def find_by_id(cls, _id) -> "ItemModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
