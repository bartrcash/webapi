from db import db

# datetime
from datetime import datetime

# models
from models.auth.user import UserModel

# flask_sqlalchemy
from flask_sqlalchemy import Pagination
from sqlalchemy.orm import backref

# typing
from typing import List
import os


class StoreModel(db.Model):

    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(80))
    image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)


    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship(
        'ItemModel', cascade="all, delete-orphan", lazy="joined")

    @classmethod
    def find_by_id(cls, _id) -> "StoreModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    @classmethod
    def get_per_page(cls, page: int) -> Pagination:

        return cls.query.paginate(page, int(os.environ.get("ITEMS_PER_PAGE")), error_out=False)

    @classmethod
    def get_by_user(cls, _user_id,  page: int) -> None:
        return cls.query.filter_by(user_id=_user_id).paginate(page, int(os.environ.get("ITEMS_PER_PAGE")), error_out=False)

    @classmethod
    def delete_by_user(cls, _user_id):
        cls.query.filter_by(user_id=_user_id).delete()
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
