# coding: utf-8
from application import db
# 文章列表

class Art(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),
                    nullable=False,
                    server_default=db.FetchedValue())
    show = db.Column(db.String(30),
                    nullable=False,
                    server_default=db.FetchedValue())
    content = db.Column(db.String(11000),
                    nullable=False,
                    server_default=db.FetchedValue())
    date = db.Column(db.DateTime,
                    nullable=False,
                    server_default=db.FetchedValue())
    remake = db.Column(db.String(500),
                    nullable=False,
                    server_default=db.FetchedValue())
    imgUrl = db.Column(db.String(255),
                    nullable=False,
                    server_default=db.FetchedValue())
    type = db.Column(db.String(255),
                    nullable=False,
                    server_default=db.FetchedValue())