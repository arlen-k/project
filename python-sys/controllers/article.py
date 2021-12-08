# -*- coding: utf-8 -*-
from application import db,app
import logging
from flask import Blueprint,request,make_response,Response
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON
from common.libs.DataHelper import getCurrentTime
from common.models.article import Art
import os,time
from common.models.user import User
from common.models.movie import Movie
from common.libs.UserService import UserService
from werkzeug.utils import secure_filename
from common.libs.LoginToken import login_required

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

article_page = Blueprint( "article_page",__name__ )


@article_page.route("/loginUser",methods = ["POST" ])
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

# 文章添加
@article_page.route("/addartic", methods=["GET", "POST"])
@login_required
def addartic():
    req = request.values
    # 如果参数在里面
    name = req['name'] if "name" in req else ""
    content = req['content'] if "content" in req else ""
    imgUrl = req['imgUrl'] if "imgUrl" in req else ""
    remake = req['remake'] if "remake" in req else ""
    type= req['type'] if "type" in req else ""
    show= req['show'] if "show" in req else ""
    if content is None or len(content) < 1:
        return ops_renderErrJSON(msg="请输入内容~~")

    put_msg = Art()
    put_msg.name = name
    put_msg.imgUrl = imgUrl
    put_msg.content = content
    put_msg.date = getCurrentTime()
    put_msg.remake = remake
    put_msg.type = type
    put_msg.show = show
    # 添加数据库 model 数据

    try:
        db.session.add(put_msg)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg='提交成功', data=content)


# 查询文章列表
@article_page.route("/getArtList", methods=[ "POST"])
@login_required  # 登录检测修饰器
def getArtList():
        req = request.values 
        page = req['page'] if "page" in req else ""
        size = req['size'] if "size" in req else ""
        name =  req['name'] if "name" in req else ""
        query = Art.query
        info = ''
        size = int(size)
        page = int( req['page'])
        list = []
        offset = (page - 1) * size
        limit = page * size
        queryList = query[offset:limit]
        # 是否有过滤查询功能
        if len(name) > 1:
            info = query.filter_by( name=name).all()
            if  len(info)!=0 :
                queryList = info
            else:
                queryList = []

        if len(queryList) >=1:
            for p in queryList:
                a = {
                    "id":p.id,
                    "name":p.name,
                    "time":p.date,
                    "imgUrl":p.imgUrl,
                }
                list.append(a)
        else:
            list = []
                
      
        total = query.count()
        if len(name) > 1:
            total = len(list)
        
        data = {
            "data":list,
            "page":page,
            'total':total
        }
        return ops_renderJSON(msg="查询成功",data=data)

# 删除文章
@article_page.route("/deleteArt", methods=["POST"])
@login_required
def deleteArt():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0

    if id < 1 :
       return make_response( ops_renderErrJSON( msg="数据有误~~" ))
    info =  Art.query.filter_by( id = id).first()

    if not info:
        return ops_renderErrJSON( msg="数据不存在" )
    # 删除数据
    try :
        Art.query.filter_by( id = id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg="删除成功")

# 详情
@article_page.route("/artInfo", methods=["POST"])
@login_required
def artInfo():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0

    if id < 1 :
       return make_response( ops_renderErrJSON( msg="数据有误~~" ))
    info =  Art.query.filter_by( id = id).first()
    if not info:
        return ops_renderErrJSON( msg="数据不存在" )
    data = {
        "name":info.name,
        "content":info.content,
        "imgUrl":info.imgUrl,
        "remake":info.remake,
        "type":int(info.type),
        "show":int(info.show)
    }
    return ops_renderJSON(msg="查询成功",data=data)

# 修改留言
@article_page.route("/editArt", methods=["POST"])
@login_required
def editArt():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0
    content = req['content'] if "content" in req else ""
    imgUrl = req['imgUrl'] if "imgUrl" in req else ""
    remake = req['remake'] if "remake" in req else ""
    type = req['type'] if "type" in req else ""
    show = req['show'] if "show" in req else ""
    name = req['name'] if "name" in req else ""
    if id < 1 :
        return make_response( ops_renderErrJSON( msg="数据有误~~" ))

    if content is None or len(content) < 1:
        return ops_renderErrJSON(msg="请输入内容~~")

    info = Art.query.filter_by( id = id).first()
    if info.imgUrl:
        if imgUrl!=info.imgUrl:
            # 删除数据 app.config['LOGINDATE']
            file_name = app.config['UPLOAD_IMG']+info.imgUrl
            if os.path.exists(file_name):
                os.remove(file_name)
                print('成功删除文件:', file_name)
            else:
                print('未找到此文件:', file_name)
        if not info:
            return ops_renderErrJSON( msg="数据不存在" )

    info.name = name
    info.content = content
    info.imgUrl = imgUrl
    info.updated_time = getCurrentTime()
    info.remake = remake
    info.type = type
    info.show = show
    try :
        db.session.add( info )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg="修改成功")


# 上传图片
@article_page.route("/photo/upload", methods=['POST'])
@login_required
def uploads():
    file_name = ''
    msg = ''
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        file = request.files['file']
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文 +getCurrentTime()
            #  获取当前时间戳---秒级级
            date = str(time.time()).split('.')[0]
            file_name = date+secure_filename(file.filename)
            # 保存图片
            file.save(os.path.join(app.config['UPLOAD_IMG'], file_name))
            msg="上传成功"
        else:
            msg="格式错误，请上传jpg/png格式文件"
    return ops_renderErrJSON(msg=msg,data={"name":file_name})

# 判断文件后缀是否在列表中
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[-1] in ['png', 'jpg', 'jpeg']

# 查看图片
@article_page.route("/photo/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    with open(r'D:/img/{}'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/png")
        return resp
    
# 查询视频 列表
@article_page.route("/getVideoList", methods=[ "POST"])
# @cache.cached(timeout=10) # 缓存
@login_required
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
        
        query = query.order_by( Movie.pub_date.desc())
        
       
        # # # 是否有过滤查询功能
        # if len(content) > 1:
        #     print(content)
        #     info = Movie.query.filter_by( content=content).all()
        #     if  len(info)!=0 :
        #         queryList = info
        #     else:
        #         queryList = []

        queryList = query[offset:limit]

        if len(queryList) >=1 :
            for p in queryList:
                a = {
                    "id":p.id,
                    "name":p.name,
                    "cover_pic":p.cover_pic,
                    "url":p.url,
                    'actor':p.actor,
                    'view_counter':p.view_counter,
                    'desc':p.desc,
                    'classify':p.classify,
                    'pub_date':p.pub_date
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

# 修改视频
@article_page.route("/editVideo", methods=["POST"])
@login_required
def editVideo():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0
    name = req['name'] if "name" in req else ""
    url = req['url'] if "url" in req else ""
    actor = req['actor'] if "actor" in req else ""
    desc = req['desc'] if "desc" in req else ""
    classify = req['classify'] if "classify" in req else ""
    cover_pic= req['cover_pic'] if "cover_pic" in req else ""

    if id < 1 :
       return make_response( ops_renderErrJSON( msg="数据有误~~" ))

    if name is None or len(name) < 1:
        return ops_renderErrJSON(msg="请输入内容~~")

    info = Movie.query.filter_by( id = id).first()

    if not info:
        return ops_renderErrJSON( msg="数据不存在" )

    info.pub_date = getCurrentTime()
    info.url = url
    info.name = name
    info.actor = actor
    info.updated_time = getCurrentTime()
    info.desc = desc
    info.classify = classify
    info.cover_pic = cover_pic

    try :
        db.session.add( info )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg="修改成功")


# 视频添加
@article_page.route("/addvideo", methods=["GET", "POST"])
@login_required
def addvideo():
    req = request.values
    # 如果参数在里面
    name = req['name'] if "name" in req else ""
    url = req['url'] if "url" in req else ""
    actor = req['actor'] if "actor" in req else ""
    desc = req['desc'] if "desc" in req else ""
    classify = req['classify'] if "classify" in req else ""
    cover_pic= req['cover_pic'] if "cover_pic" in req else ""

    if name is None or len(name) < 1:
        return ops_renderErrJSON(msg="请输入电影名~~")

    info = Movie()

    info.pub_date = getCurrentTime()
    info.url = url
    info.actor = actor
    info.name = name
    info.updated_time = getCurrentTime()
    info.desc = desc
    info.cover_pic = cover_pic
    info.classify = classify
    info.view_counter = 1

    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg='提交成功') 

# 删除视频
@article_page.route("/deleteVideo", methods=["POST"])
@login_required
def deleteVideo():
    req = request.values 
    id = int( req['id'] )  if ( 'id' in req and req['id'] ) else 0

    if id < 1 :
       return make_response( ops_renderErrJSON( msg="数据有误~~" ))
    info =  Movie.query.filter_by( id = id).first()

    if not info:
        return ops_renderErrJSON( msg="数据不存在" )
    # 删除数据
    try :
        Movie.query.filter_by( id = id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e

    return ops_renderJSON(msg="删除成功")
