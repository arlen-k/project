# -*- coding: utf-8 -*-
from application import app


from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension( app )

'''
拦截器处理 和 错误处理器
'''
from interceptors.Auth import *
from interceptors.errorHandler import *

'''
蓝图
'''
from controllers.index import index_page
from controllers.member import member_page
from controllers.article import article_page
app.register_blueprint( index_page,url_prefix = "/" )
app.register_blueprint( member_page,url_prefix = "/member" )
app.register_blueprint( article_page,url_prefix = "/artic" )

'''
模板函数
'''
from common.libs.UrlManager import UrlManager
app.add_template_global( UrlManager.buildStaticUrl,'buildStaticUrl' )
app.add_template_global( UrlManager.buildUrl,'buildUrl' )