# PaKe爬客网

分布式爬虫系统

演示网址：http://120.79.204.134 测试账号：ceshi,密码：aaa123456

演示视频：https://www.bilibili.com/video/av23277874/


## 选题依据

6月29日，马云说，大家还没搞清PC时代的时候，移动互联网来了，还没搞清移动互联网的时候，大数据时代来了。这次选题的依据就是在这个大数据的背景下，我们进行数据分析得出相对准确的分析结果。我们选择的方向是淘宝、天猫电商平台、加上趣味的歌手音乐数据的获取与分析，数据获取固然十分重要，但是数据的清洗与分析就让这些数据起到如虎添翼的作用，可以根据这些信息商家做出相应的调整战略。


## 技术路线

爬客网是基于python中scrapy-redis框架打造的分布式爬虫，极大的提高爬取数据的速率，前端页面的展示运用了django框架，前端的设计则用了Bootstrap，技术路线首先是数据获取：scrapy+xpath(正则表达式)爬取页面--scrapy模拟登陆天猫（选择带cookie突破天猫的反爬虫的功能）--为了提高爬取速度，运用scrapy-redis进行分布式爬虫（Master和Salver数据的调度）--存储数据选择运用mongodb（key-value类型的数据库有利于提高查找数据的速度）--突破反爬虫（1：更改爬虫头部信息，模拟浏览器爬虫:2：有进行限制爬取的速度，不允许过快:3：选择模拟登陆天猫带cookie爬虫，解决302暂时性重定向导致无法爬取到想要的信息4：ip代理），前端用了django框架进行页面的显示，html编写用Bootstrap前端开发工具包
  
  
## 方案设计

1、设计要求分析：不同用户能够有自己相对应的账号进入爬客网的网页
（包括移动端），进入网页能够选择1：任务发布、2：查看任务3：导出数据4：分析数据生成可视化图表5：数据要求去重（质量高）

2、系统功能：爬客网在线支持人数合理，系统并发要尽量满足用户需求

3、原理方案设计：模拟访问淘宝、天猫电商平台，输入关键词生成url进行url解析，生成的店铺入口运用redis分发发给不同的Slave进行爬取任务，爬取好数据存储在mongodb然后前端进行提取数据，并进行数据的解析生成可视化的图表，在前端展示给用户看


## 环境需求
### 环境
Python2.7 + mysql + mongodb + anaconda + redis

### 组件
scrapy,
requests,
chardet,
web.py, 
sqlalchemy, 
gevent, 
psutil, 
django==1.11 (注意版本号，高于1.11的版本可能不支持python2.7),
redis, 
python-redis, 
pymongo, 
twisted, 
scrapy-redis,

......
还有好多好多，（包括mysql的支持模块、生成地图的模块等等）大家看情况报什么错就打什么包吧

### 执行步骤:
第一步：启动mongodb服务

  mongod
  
第二步：启动redis服务

  redis-server.exe redis.windows.conf
  
  redis-cli.exe -h 127.0.0.1 -p 6379
  
第三步:部署Master端

  scrapy crawl taobaoMaster
  
第四步：部署Slave端

  scrapy crawl taobao
  
第五步：部署可视化端（django）

  python manage.py runserver
  
  访问http://ip:port/(默认：http://localhost:8000/)
  
第六步（可选）：部署爬虫监控端

  python app.py
  
  访问http://ip:port/show(默认：http://localhost:8080/show)
  
其他步骤包括数据迁移，以及修改mysql和mongodb账号密码这我就不一一说明了


## 总结

这个项目的成功开发离不开每一个组员的努力，从一开始我把他们召集起来，说出来我的这个爬虫的想法到后来的每个星期、每天的开发，看博客找资料，改bug优化，到后来项目的初步实现，我们确实克服了挺多的困难，在学习知识的过程是有喜与悲，这个项目需要具备的知识我们学习起来或许并不是特别的吃力，难的是如何将整个系统有条理的开发出来。最后感谢小组其他两位队员，感觉老师的观看，谢谢。


## 作者简介

小组成员：姜发健、秦俊涛、王博

联系邮箱：793740385@qq.com
