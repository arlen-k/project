# -*- coding: utf-8 -*-
from application import app,db,cache
from flask import Blueprint,request,make_response,redirect,Response
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON,ops_render
from common.libs.DataHelper import getCurrentTime
from common.libs.UrlManager import UrlManager
from common.models.user import User
from common.libs.UserService import UserService
from common.models.message import Msg
from common.models.movie import Movie
from sqlalchemy.sql.expression import func
import json,os,time
member_page = Blueprint( "member_page",__name__ )


def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))

def default(self, obj):
    if isinstance(obj, bytes):
        return str(obj, encoding='utf-8')

    return json.JSONEncoder.default(self, obj)

# 视频添加
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
@member_page.route("/getVideoList", methods=[ "POST"])
# @cache.cached(timeout=10) # 缓存
def getVideoList():
        req = request.values 
        page = req['page'] if "page" in req else ""
        size = req['size'] if "size" in req else ""
        content =  req['content'] if "content" in req else ""
        query = Movie.query
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

