# 电影网系统管理 分为三个端 ： pc电脑端、 后台系统、 服务系统 
 在线观看：http://tv.arlen.top
 后台系统：http://tv.arlen.top:8081/#/login
 可视化后台管理，一键式脚本自动化部署抓取，自动化部署linux，给你高大上的操作体验
（仓库为综合类型,研究学习项目，主要放置有意思的代码，感兴趣的朋友可以下载看看）

![image](https://user-images.githubusercontent.com/31032218/147064836-b0e3f2cd-2b0c-48a0-b613-62b18c445329.png)
![image](https://user-images.githubusercontent.com/31032218/147064848-d3ba56b3-5f08-47a1-ab2a-7d9ac8a695c5.png)

主要涉及技术：

    1.后端：python + flask + flask-sqlalchemy + requests +  Blueprint + tornado
    2.前端：vue + element + sass + axios + vuex + echarts +  Tinymce +webpack
    3.电影web： Bootstrap + Jq + ajax + css + h5
    4.前端自动化部署：node + shelljs + ssh2-sftp-client  + nginx
    5.爬虫：selenium + BeautifulSoup4 + requests

# 一、仓库项目 python-sys （安装python环境）

 1.为python编写的后台服务，涉及电影网站pc端页面model和电影网站后台系统的所有前端接口。

 2.项目框架可以二次开发，在此token的登录劫持和过期设置都已经通过配置文件提取在 config文件里面,后台系统和前端访问的代码皆已分离

 3.下载 ：pip install -r common/requirements.txt 

 4.下载：pip install -i https://pypi.douban.com/simple virtualenvwrapper-win   此方式可以快速下载插件

 5.启动服务项目：python manager.py runserver 项目启动后建议用 nginx 做反向代理配置

 6.卸载：pip uninstall -r modules.txt -y
 
 7. 配置数据库时候，注意修改config/local_setting.py  里面的SQLALCHEMY_DATABASE_URI 这里 是整个后端项目的数据库配置，修改即可

 目录介绍：
    common 数据库model  
    config 环境配置  
    controllers 业务代码逻辑  
    interceptors 前端访问拦截器  
    jobs 爬虫脚本存放
    static pc访问端模板 js方法集合库  
    templates pc访问端模板  

# 二、仓库项目 vue-web-sys （安装node环境）

 1.项目为电影网站的后台管理系统，主要有电影的增删改查，账号登录。后期涉及的数据统计和博客的文章发布等功能，接口都在逐步完善中。

 2.拉取项目 后 安装启动项目的依赖  安装淘宝镜像 npm i -g cnpm --registry=https://registry.npm.taobao.org

 3.执行 cnpm i   

 4.启动项目 npm run serve 进入 login 页面登录 账号密码默认可查看

 5.新增部署自动化部署脚本  upload config 自行配置服务器 npm run upload 自动提交

 目录介绍：
    api 接口库  
    assets 图片和初始全局样式  
    components 组件库  
    router 路由  
    store 状态管理器  
    utils 方法库  
    views 业务代码处和测试代码集合处  

# 三、爬虫脚本 python
1、爬虫脚本为python ，核心采用技术 selenium + BeautifulSoup4 + requests 
2、selenium 需要配置本地环境 采用 windows版本，这个可用于自动化测试脚本使用，配置好了 ，使用起来非常酷炫。 
3、本地驱动文件我已经 放入 python-sys/jobs chromedriver.exe，使用需要配置这个环境，本脚本采用谷歌 ，记得下载谷歌浏览器。
4、爬虫的网站来源网络随便找的 电影网，但是资源非常不错（注意：仅仅用于学习，注意爬虫动态抓取的时间控制，不要把人家服务器搞崩了）。

# nginx
 配置文件放在utils 各位使用者需要自行下载nginx在各自的环境版本，配置参考我的即可，使用和启动方式需要百度自行学习
 
# 更新 2021.12.30 版本会不间断更新~   

（路漫漫其修远兮，吾将上下而求索）
