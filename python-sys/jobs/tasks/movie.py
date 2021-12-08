# -*- coding: utf-8 -*-
from application import app,db
import requests,os,time,hashlib,json,re
from bs4 import BeautifulSoup
from common.libs.DataHelper import getCurrentTime
from urllib.parse import urlparse
from common.models.movie import Movie
'''
python manager.py runjob -m movie -a list | parse
'''
class JobTask():
    def __init__(self):
        self.source = "btbtdy"
        self.url = {
            "num" : 3,
            "url" : "http://www.btbtdy.me/btfl/dy1-#d#.html",
            "path" : "/tmp/%s/" %( self.source )
        }

    '''
    第一步 首先 获取列表list html 回来，通过解析html 获取详情 的 url等信息，在根据详情url 获取详情html
    第二步 解析 详情的html
    '''
    def run(self,params):
        act = params['act']
        self.date = getCurrentTime( frm = "%Y%m%d")
        if act == "list":
            self.getList()
            self.parseInfo()
        elif act == "parse":
            self.parseInfo()

    '''
    获取列表
    '''
    def getList(self):
        config = self.url
        path_root = config['path'] + self.date
        path_list = path_root + "/list"
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        path_vid = path_root + "/vid"
        self.makeSuredirs( path_root )
        self.makeSuredirs( path_list )
        self.makeSuredirs( path_info )
        self.makeSuredirs( path_json )
        self.makeSuredirs( path_vid )

        pages = range( 1,config['num'] + 1 )
        for idx in pages:
            tmp_path = path_list + "/" + str( idx )
            tmp_url = config['url'].replace("#d#",str( idx ) )
            app.logger.info( "get list : " +  tmp_url )
            if os.path.exists( tmp_path ):
                continue

            tmp_content = self.getHttpContent( tmp_url )
            self.saveContent( tmp_path,tmp_content )
            time.sleep(0.3)

        for idx in os.listdir( path_list ):
            tmp_content = self.getContent( path_list + "/" + str( idx ) )
            items_data = self.parseList( tmp_content )
            if not items_data:
                continue

            for item in items_data:
                tmp_json_path = path_json + "/" + item['hash']
                tmp_info_path = path_info + "/" + item['hash']
                tmp_vid_path = path_vid + "/" + item['hash']
                if not os.path.exists( tmp_json_path ):
                    self.saveContent( tmp_json_path, json.dumps( item,ensure_ascii=False ) )

                if not os.path.exists(tmp_info_path):
                    tmp_content = self.getHttpContent( item['url'] )
                    self.saveContent(  tmp_info_path,tmp_content )

                if not os.path.exists( tmp_vid_path ):
                    tmp_content = self.getHttpContent( item['vid_url'] )
                    self.saveContent(  tmp_vid_path,tmp_content )

                time.sleep( 0.3 )


    def parseList(self,content):
        data = []
        config = self.url
        url_info = urlparse( config['url'] )
        url_domain = url_info[0] + "://" + url_info[1]

        tmp_soup = BeautifulSoup( str(content),"html.parser" )
        tmp_list = tmp_soup.select( "div.list_su ul li" )
        for tmp_item in tmp_list:
            tmp_target = tmp_item.select("a.pic_link")
            tmp_name = tmp_target[0]['title']
            tmp_href = tmp_target[0]['href']
            if "http:" not in tmp_href:
                tmp_href = url_domain + tmp_href
            tmp_vid_url = tmp_href.replace("btdy/dy", "vidlist/")
            tmp_data = {
                "name" : tmp_name,
                "url" : tmp_href,
                "vid_url" : tmp_vid_url,
                "hash" :  hashlib.md5( tmp_href.encode("utf-8") ).hexdigest()
            }
            data.append( tmp_data )

        return data

    '''
    解析详情信息
    '''
    def parseInfo(self):
        config = self.url
        path_root = config['path'] + self.date
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        path_vid = path_root + "/vid"
        for filename in os.listdir(  path_info ):
            tmp_json_path = path_json + "/" + filename
            tmp_info_path = path_info + "/" + filename
            tmp_vid_path = path_vid + "/" + filename

            tmp_data = json.loads( self.getContent( tmp_json_path) ,encoding="utf-8")
            tmp_content = self.getContent( tmp_info_path )
            tmp_soup = BeautifulSoup( tmp_content,"html.parser")
            try:
                tmp_pub_date = tmp_soup.select( "div.vod div.vod_intro dl dd" )[0].getText()
                tmp_desc = tmp_soup.select( "div.vod div.vod_intro div.des" )[0].getText()
                tmp_classify = tmp_soup.select( "div.vod div.vod_intro dl dd" )[2].getText()
                tmp_actor = tmp_soup.select( "div.vod div.vod_intro dl dd" )[6].getText()
                tmp_pic_list = tmp_soup.select("div.vod div.vod_img img")
                tmp_pics = []
                for tmp_pic in tmp_pic_list:
                    tmp_pics.append( tmp_pic['src'] )

                #获取下载地址
                tmp_download_content = self.getContent( tmp_vid_path  )
                tmp_vid_soup = BeautifulSoup( tmp_download_content ,"html.parser")
                tmp_download_list = tmp_vid_soup.findAll( "a",href = re.compile( "magnet:?" ) )
                tmp_magnet_url = ""
                if tmp_download_list:
                    tmp_magnet_url = tmp_download_list[0]['href']


                tmp_data['pub_date'] = tmp_pub_date
                tmp_data['desc'] = tmp_desc
                tmp_data['classify'] = tmp_classify
                tmp_data['actor'] = tmp_actor
                tmp_data['magnet_url'] = tmp_magnet_url
                tmp_data['source'] = self.source
                tmp_data['created_time'] = tmp_data['updated_time'] = getCurrentTime()
                if tmp_pics:
                    tmp_data['cover_pic'] = tmp_pics[0]
                    tmp_data['pics'] = json.dumps( tmp_pics )

                tmp_movie_info = Movie.query.filter_by( hash  = tmp_data['hash']).first()
                if tmp_movie_info:
                    continue

                tmp_model_movie = Movie( **tmp_data )
                db.session.add( tmp_model_movie )
                db.session.commit()
            except:
                continue
        return True

    def getHttpContent(self,url):
        try:
            r = requests.get( url )
            if r.status_code != 200 :
                return None

            return r.content

        except Exception:
            return None

    def saveContent(self,path,content):
        if content:
            with open( path,mode="w+",encoding="utf-8" ) as f:
                if type(content) != str:
                    content = content.decode("utf-8")

                f.write(content )
                f.flush()
                f.close()

    def getContent(self,path):
        if os.path.exists( path ):
            with open( path ,"r") as  f:
                return f.read()

        return ''

    def makeSuredirs(self,path):
        if not os.path.exists( path ):
            os.makedirs( path )