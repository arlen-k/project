# # -*- coding: utf-8 -*-
from application import app
from flask import  request,g,jsonify  
from common.models.user import User
from common.libs.UserService import UserService
from common.libs.Helper import ops_renderErrJSON
import time

# '''
# 判断用户是否登录
# '''
def getDefaultUrl(path):
    urls = path.split('/')
    urlList = "/%s/%s"%(urls[1],urls[2]) 
    return urlList

@app.before_request
def before_request():
   
    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info
    return



@app.after_request
def after_request( response ):
    return response

'''
判断用户是否登录
'''
def check_login():
    cookies = request.cookies
    cookie_name = app.config['AUTH_COOKIE_NAME']
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len( auth_info ) != 2:
        return False

    try:
        user_info = User.query.filter_by( id = auth_info[1] ).first()
    except Exception :
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode( user_info ):
        return False

    return user_info