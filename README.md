# 电影网系统管理 sys+h5+pc ， 仓库为综合类型，主要放置有意思的代码，感兴趣的朋友可以下载看看

主要涉及技术：
    1.后端：python + flask + flask-sqlalchemy + mysqlclient + requests + BeautifulSoup4 + Blueprint
    2.前端：vue + element + sass + axios + vuex + echarts + eslint

# 一、仓库项目 python-sys （安装python环境）

 1.为python编写的后台服务，涉及电影网站pc端页面model和电影网站后台系统的所有前端接口。

 2.项目框架可以二次开发，在此token的登录劫持和过期设置都已经通过配置文件提取在 config文件里面,后台系统和前端访问的代码皆已分离

 3.下载 ：pip install -r common/requirements.txt 

 4.下载：pip install -i https://pypi.douban.com/simple virtualenvwrapper-win   此方式可以快速下载插件

 5.启动服务项目：python manager.py runserver

 6.卸载：pip uninstall -r modules.txt -y

# 二、仓库项目 vue-web-sys （安装node环境）

 1.项目为电影网站的后台管理系统，主要有电影的增删改查，账号登录。后期涉及的数据统计和博客的文章发布等功能，接口都在逐步完善中。

 2.拉取项目 后 安装启动项目的依赖  安装淘宝镜像 npm i -g cnpm --registry=https://registry.npm.taobao.org

 3.执行 cnpm i   

 4.启动项目 npm run serve 进入 login 页面登录 账号密码默认可查看