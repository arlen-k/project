import time 
import functools
from flask import g,request
from common.models.user import User
from common.libs.UserService import UserService
from common.libs.Helper import ops_renderErrJSON

'''
判断用户是否登录 局部使用 本功能用于学习
'''
def check_login():
    # cokies 不能跨越，headers token 可以 系统用header 网站用cookie
    # cookies = request.cookies
    # cookie_name = app.config['AUTH_COOKIE_NAME']
    # auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    auth_cookie = ''
    if 'token' in request.headers:
        auth_cookie = request.headers.get('token')

    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len( auth_info ) != 3:
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

#在上面的基础上导入
def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        token =  request.headers.get('token') 
        if token:
            #在请求头上拿到token
            user_info = check_login()
            if user_info:
                g.current_user = user_info
            else:
                return ops_renderErrJSON(code = 401,msg = "未登录")  

            if 'token' in request.headers:
                auth_cookie = token
                auth_info = auth_cookie.split("#")

                if len( auth_info ) != 3:
                    return ops_renderErrJSON(code = 400,msg = '登录信息错误，重新登录')
                
                if float(auth_info[2]) < time.time():
                    return ops_renderErrJSON(code = 401,msg = "登录已过期")     
            
        else:
            #没接收的到token,给前端抛出错误
            return ops_renderErrJSON(code = 403,msg = '缺少参数token')

        return view_func(*args,**kwargs)
    return verify_token