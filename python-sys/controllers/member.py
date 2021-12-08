# -*- coding: utf-8 -*-
from application import app,db
from flask import Blueprint,request,make_response,redirect,Response
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON,ops_render,iPagenation
from common.libs.DataHelper import getCurrentTime
from common.libs.UrlManager import UrlManager
from common.models.user import User
from common.libs.UserService import UserService
from common.models.message import Msg
from common.models.movie import Movie
from sqlalchemy.sql.expression import func
import json,os,time,re
from common.libs.LoginToken import login_required

member_page = Blueprint( "member_page",__name__ )


def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))


@member_page.route("/seaViedo",methods = [ "GET","POST" ])
def seaViedo():
    req = request.values
    name = req['name'] if "name" in req else ""
    print(name)
    page = 1
    if 'p' in req and req['p']:
        page = int( req['p'] )
    
    query = Movie.query
    query= query.filter_by( name = name).all()
    page_params = {
        'total_count':10,
        "page_size":12,
        'page':page,
        'url': "/seaViedo?"
    }

    pages = iPagenation( page_params )
    # 0 - 30,30 - 60 ,60 - 90
    
    offset = ( page - 1 ) * page_params['page_size']
    limit = page * page_params['page_size']

    list_movie = query[offset:limit]
    
    return ops_render( "member/seaViedo.html", { "data":list_movie,"pages":pages })

# 注册
@member_page.route("/reg",methods = [ "GET","POST" ])
def reg():
    if request.method == "GET":
        return ops_render("member/reg.html")

    req = request.values
    nickname = req['nickname'] if "nickname" in req else ""
    login_name = req['login_name'] if "login_name" in req else ""
    login_pwd = req['login_pwd'] if "login_pwd" in req else ""
    login_pwd2 = req['login_pwd2'] if "login_pwd2" in req else ""

    if login_name is None or len( login_name ) < 1:
        return ops_renderErrJSON( msg = "请输入正确的登录用户名~~" )

    if login_pwd is None or len( login_pwd ) < 6:
        return ops_renderErrJSON( msg ="请输入正确的登录密码，并且不能小于6个字符~~")

    if login_pwd != login_pwd2:
        return ops_renderErrJSON(msg="请输入正确的确认登录密码~~")

    user_info = User.query.filter_by( login_name = login_name ).first()
    if user_info:
        return ops_renderErrJSON( msg ="登录用户名已被注册，请换一个~~")

    model_user = User()
    model_user.login_name = login_name
    model_user.nickname = nickname if nickname is not None else login_name
    model_user.login_salt = UserService.geneSalt( 8 )
    model_user.login_pwd = UserService.genePwd( login_pwd,model_user.login_salt )
    model_user.created_time = model_user.updated_time = getCurrentTime()
    db.session.add( model_user )
    db.session.commit()
    return ops_renderJSON( msg = "注册成功~~" )

@member_page.route("/login",methods = [ "GET","POST" ])
def login():
    if request.method == "GET":
        return ops_render("member/login.html")

    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    if login_name is None or len( login_name ) < 1:
        return ops_renderErrJSON(  "请输入正确的登录用户名~~" )

    if login_pwd is None or len( login_pwd ) < 6:
        return ops_renderErrJSON("请输入正确的登录密码~~")
    user_info = User.query.filter_by( login_name = login_name ).first()
    if not user_info:
        return ops_renderErrJSON("请输入正确的登录用户名和密码 -1~~")

    if user_info.login_pwd != UserService.genePwd( login_pwd,user_info.login_salt ):
        return ops_renderErrJSON("请输入正确的登录用户名和密码 -2 ~~")
    user_info.status = int(user_info.status)
    if user_info.status != 1:
        return ops_renderErrJSON( "账号被禁用，请联系管理员处理~~" )

    #session['uid'] = user_info.id
    
    response = make_response( ops_renderJSON( msg="登录成功~~" ) )
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],
                        "%s#%s"%( UserService.geneAuthCode( user_info ),user_info.id ),60 * 60 *24 *120 )
    return response


@member_page.route("/loginUser",methods = ["POST" ])
def loginUser():
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    if login_name is None or len( login_name ) < 1:
        return make_response(  ops_renderErrJSON( msg="请输入正确的登录用户名~~" ))

    if login_pwd is None or len( login_pwd ) < 6:
        return make_response( ops_renderErrJSON( msg="登录密码错误~~" ))

    user_info = User.query.filter_by( login_name = login_name ).first()

    if not user_info:
        return make_response( ops_renderErrJSON(msg="请输入正确的登录用户名 -1~~"))

    if user_info.login_pwd != UserService.genePwd( login_pwd,user_info.login_salt ):
        return ops_renderErrJSON(msg="请输入正确的登录密码 -2 ~~")
    
    user_info.status = int(user_info.status)
    if user_info.status != 1:
        return ops_renderErrJSON( msg="账号被禁用，请联系管理员处理~~")
    
    info = {
        "name":user_info.nickname,
        "id":user_info.id,
    }
    
    ts_str = str(int(time.time()) + app.config['LOGINDATE'] )
    # ts_byte = ts_str.encode("utf-8")
    # print('当前主机名称为 : ' + socket.gethostname())
    # print('当前主机的IP为: ' + socket.gethostbyname(socket.gethostname()))
    # 变量字符串拼接
    token = "%s#%s#%s"%( UserService.geneAuthCode( user_info ),user_info.id,ts_str) 
    content = {
        "token":token,
        "info": info
    }
    
    return ops_renderJSON( msg="登录成功~~", data=content ) 


# 退出登录
@member_page.route("/logout")
def logOut():
    response = make_response( redirect( UrlManager.buildUrl("/") ) )
    response.delete_cookie(  app.config['AUTH_COOKIE_NAME'] )
    return response

# 查看详情
@member_page.route("/info", methods=["GET"])
def info():
    req = request.values
    # app.logger.info( req['id'] )
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0
    if id < 1 :
        return redirect( UrlManager.buildUrl("/") )
    
    info = Movie.query.filter_by( id = id).first()
    if not info:
        return redirect(UrlManager.buildUrl("/"))
    '''
    更新阅读数量
    '''
    num = int(info.view_counter) 
    num+= 1
    info.view_counter = num
    db.session.add( info )
    db.session.commit()

    '''
    获取推荐
    '''
    recommend_list = Movie.query.order_by( func.rand() ).limit( 4 )
    return ops_render("member/info.html",{ "info":info,"recommend_list":recommend_list })

# 播放视频
@member_page.route("/paly", methods=["GET"])
def paly():
    req = request.values
  
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0
    if id < 1 :
        return redirect( UrlManager.buildUrl("/") )
    
    info = Movie.query.filter_by( id = id).first()
    if not info:
        return redirect(UrlManager.buildUrl("/"))

    '''
    获取推荐
    '''
    recommend_list = Movie.query.order_by( func.rand() ).limit( 4 )

    return ops_render("member/play.html",{ "info":info,"recommend_list":recommend_list })

def default(self, obj):
    if isinstance(obj, bytes):
        return str(obj, encoding='utf-8')

    return json.JSONEncoder.default(self, obj)

# 留言
@member_page.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "GET":
        result = Msg.query.all()
        query = Msg.query
        context = {
            "result":result,
            "pages":{
                "total":query.count(),
                "page_size":10
            }
        }
        return ops_render("member/message.html", context)

    req = request.values
    # 如果参数在里面
    content = req['content'] if "content" in req else ""
    name = req['name'] if "name" in req else ""
    imgUrl = req['imgUrl'] if "imgUrl" in req else ""
    if content is None or len(content) < 1:
        return ops_renderErrJSON(msg="请输入内容~~")
    put_msg = Msg()
    put_msg.name = name
    put_msg.imgUrl = imgUrl
    put_msg.content = content
    put_msg.updated_time = getCurrentTime()
    # 添加数据库 model 数据

    try:
        db.session.add(put_msg)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg='提交成功', data=content)

# 查询留言意见 列表
@member_page.route("/getMsgList", methods=[ "POST"])
# @cache.cached(timeout=10) # 缓存
def getMsgList():
        req = request.values 
        page = req['page'] if "page" in req else ""
        size = req['size'] if "size" in req else ""
        content =  req['content'] if "content" in req else ""
        query = Msg.query
        info = ''

        size = int(size)
        page = int( req['page'])
        list = []
        offset = (page - 1) * size
        limit = page * size
        queryList = query[offset:limit]
        # 是否有过滤查询功能
        if len(content) > 1:
            info = query.filter_by( content=content).all()
            if  len(info)!=0 :
                queryList = info
            else:
                queryList = []

        if len(queryList) >=1 :
            for p in queryList:
                a = {
                    "id":p.id,
                    "name":p.name,
                    "content":p.content,
                    "time":p.updated_time,
                    "imgUrl":p.imgUrl,
                }
                list.append(a)
        else:
            list = []
                
      
        total = query.count()
        if len(content) > 1:
            total = len(list)
        
        data = {
            "data":list,
            "page":page,
            'total':total
        }
        return ops_renderJSON(msg="查询成功",data=data)

# 删除留言
@member_page.route("/deleteMsg", methods=["POST"])
@login_required
def deleteMsg():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0
    
    if id < 1 :
       return make_response( ops_renderErrJSON( msg="数据有误~~" ))
    
    info =  Msg.query.filter_by( id = id).first()

    if not info:
        return ops_renderErrJSON( msg="数据不存在" )
    
    # 删除数据
    file_name = "D:/img/"+info.imgUrl
    if os.path.exists(file_name):
        os.remove(file_name)
        print('成功删除文件:', file_name)
    else:
        print('未找到此文件:', file_name)
    
    try :
        Msg.query.filter_by( id = id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg="删除成功")

# 修改留言
@member_page.route("/editMsg", methods=["POST"])
@login_required
def editMsg():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0
    content = req['content'] if "content" in req else ""
    imgUrl = req['imgUrl'] if "imgUrl" in req else ""
    if id < 1 :
       return make_response( ops_renderErrJSON( msg="数据有误~~" ))

    if content is None or len(content) < 1:
        return ops_renderErrJSON(msg="请输入内容~~")

    info = Msg.query.filter_by( id = id).first()

    if not info:
        return ops_renderErrJSON( msg="数据不存在" )
    
    info.content = content
    info.imgUrl = imgUrl
    info.updated_time = getCurrentTime()
    
    try :
        db.session.add( info )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg="修改成功")

