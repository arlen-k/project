'''
Description: 
Version: 2.0
Autor: 作者博客：www.arlen.top
Date: 2021-07-20 10:28:03
LastEditors: Seven
LastEditTime: 2021-11-16 16:07:08
'''
# -*- coding: utf-8 -*-
#本地开发环境配置文件
from config.base_setting import *

SQLALCHEMY_DATABASE_URI="mysql://root:zkh123456@127.0.0.1/python?charset=utf8" # 线上"mysql://root:root@127.0.0.1/python?charset=utf8"
AUTH_COOKIE_NAME = 'token'
SQLALCHEMY_POOL_RECYCLE = -1
DOMAIN = { 
    "www":"http://127.0.0.1:80" # 线上"http://tv.arlen.top" 
} 
UPLOAD_IMG = 'D:/img/'

LOGINDATE = 60  * 60 * 12 * 5 # token 系统时间