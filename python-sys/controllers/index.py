# -*- coding: utf-8 -*-
from flask import Blueprint,request,redirect
from common.models.movie import Movie
from application import app,db
from common.libs.Helper import ops_render,iPagenation,print_json
from common.libs.UrlManager import UrlManager
from sqlalchemy.sql.expression import func


index_page = Blueprint( "index_page",__name__ )

@index_page.route("/")
def index():
    req = request.values
    order_by_f = str(req['order']) if ( "order" in req and req['order'] ) else "lastest"
    page = 1
    if 'p' in req and req['p']:
        page = int( req['p'] )

    query = Movie.query

    page_params = {
        'total_count':query.count(),
        "page_size":12,
        'page':page,
        'url': "/?"
    }
    # print(page_params)
    pages = iPagenation( page_params )
    
    # 0 - 30,30 - 60 ,60 - 90
    offset = ( page - 1 ) * page_params['page_size']
    limit = page * page_params['page_size']

    if order_by_f == "hot":
        query = query.order_by( Movie.view_counter.desc(),Movie.id.desc() )
    else:
        query = query.order_by( Movie.pub_date.desc(),Movie.id.desc() )

    list_movie = query[offset:limit]

    return ops_render( "index.html", { "data":list_movie,"pages":pages })


