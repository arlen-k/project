# -*- coding: utf-8 -*-
import re
from flask import jsonify,g,render_template,request
import math
import json

def ops_render( template,context = {} ):
    if 'current_user' in  g:
        context['current_user'] = g.current_user
    return render_template( template, **context )

def ops_renderJSON( code = 200,msg = "操作成功~~",data = {} ):
    resp = { "code":code,"msg":msg,"data":data }
    return jsonify( resp )

def ops_renderErrJSON(code = -1, msg = "系统繁忙，请稍后再试~~",data = {} ):
    return ops_renderJSON( code=code,msg = msg,data = data )
    
def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))

# 判断文件后缀是否在列表中
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[-1] in ['png', 'jpg', 'jpeg']

def iPagenation( params):
    total_count = int( params['total_count'] )
    page_size = int( params['page_size'] )
    page = int( params['page'] )

    total_pages = math.ceil(total_count / page_size)
    total_pages = total_pages if total_pages > 0 else 1

    is_prev = 0 if page <= 1 else 1
    is_next = 0 if page >= total_pages else 1
    pages = {
        'current':page,
        'total_pages':total_pages,
        'total':total_count,
        'page_size':page_size,
        'is_next': is_next,
        'is_prev': is_prev,
        'range': range( 1,total_pages + 1 ),
        'url':params['url']
    }
    # range(10)        # 从 0 开始到 10
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return pages