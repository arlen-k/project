'''
Description: 
Version: 2.0
Autor: 作者博客：www.arlen.top
Date: 2021-07-20 10:28:02
LastEditors: Seven
LastEditTime: 2021-11-16 15:13:26
'''
# -*- coding: utf-8 -*-
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import local_setting
from flask_redis import FlaskRedis


# from flask_cache  import Cache
# import os

app = Flask( __name__ )
manager = Manager( app )
app.config.from_object(local_setting)
# app.debug = True

rd = FlaskRedis(app)

# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
# app.config.from_pyfile( "config/local_setting.py" )
# ops_config=local|production
# linux export ops_config=local|production
# windows set ops_config=local|production
# print(os.environ)
# if "ops_config" in os.environ:
#     app.config.from_pyfile( "config/%s_setting.py"%( os.environ['ops_config'] ) )

db = SQLAlchemy( app )
