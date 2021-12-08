# coding: utf-8
from application import db


class Msg(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),
                     nullable=False,
                     server_default=db.FetchedValue())
    imgUrl = db.Column(db.String(30),
                     nullable=False,
                     server_default=db.FetchedValue())
    content = db.Column(db.String(500),
                        nullable=False,
                        server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime,
                             nullable=False,
                             server_default=db.FetchedValue())
