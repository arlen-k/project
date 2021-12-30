# 最新脚本windows版本
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from application import db 
from common.libs.DataHelper import getCurrentTime
from common.models.movie import Movie

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'} 

http_url = 'http://n.9do9.com'

chrome_driver=r"C:\Users\EDZ\AppData\Local\Programs\Python\Python39\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"

def getHtml(url):
    resp = requests.get(url, headers=headers) 
    resp.raise_for_status()
    resp.encoding="utf-8"
    return resp.text

# 获取内容
def getContent(con):
    tmp_soup = BeautifulSoup(str(con), "html.parser")
    return tmp_soup

 # 获取列表
def run():
   
    resp = getHtml(web_url)
    tmp_soup = getContent(resp)
    # 通过http 获取页面详情
    page = tmp_soup.select("div.stui-pannel_bd ul li")

    index = 0
    for tmp_item in page:
        # 电影名字
        tmp_name = tmp_item.select("h4")[0].getText()
        # 电影详情链接
        tmp_href = http_url + tmp_item.select("a")[0]['href']
        # 电影图片
        tmp_img = tmp_item.select("a")[0]['data-original']
        # 主演
        tostar = tmp_item.select("p")[0].getText()
        
        # 第二层
        # 具体电影详情
        listInfo = getHtml(tmp_href)
        info = getContent(listInfo)
        # # 获取详情简介
        introduction = info.select_one("span.detail-content").getText()
        # # 电影类型
        types = info.select("p.data")[2].getText().split('：')[1]
        infolink =  http_url + info.select_one("a.btn-primary")['href'] 

        # 第三层  获取播放链接
        browser=webdriver.Chrome(executable_path=chrome_driver) #2.通过浏览器向服务器发送URL请求
        browser.get(infolink)
        info3 = getContent(browser.page_source)  # BeautifulSoup(browser.page_source, 'html.parser')
        url = ''
        if info3:
            url = info3.select_one("div.stui-player__video iframe.embed-responsive-item")['src']
            
        browser.quit()

        infos = Movie()
        # 存入数据库
        infos.name = tmp_name
        infos.classify = types
        infos.actor = tostar
        infos.url = url
        infos.view_counter = 0
        infos.cover_pic = tmp_img
        infos.desc = introduction
        infos.pub_date =getCurrentTime()
        infos.updated_time =getCurrentTime()
        
        try:
            db.session.add(infos)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return e
        
        index = index + 1
        if(index==2):
            break;


for item in range(5):
    nums = item + 1
    web_url = http_url+'/?m=vod-type-id-1-pg-'+ str(nums) +'.html'
    run()
   