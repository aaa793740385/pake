# _*_coding:utf-8_*_
import requests
import sys

#这个类的作用是通过代理池在https中提取进行访问网站所需的ip地址与端口
def GetIps():
    list = []
    global count
    url = url ='http://127.0.0.1:8000/?types=0&count=300'
    ips = requests.get(url)     #访问该网站

    #eval用法是str当做一个函数进行计算
    for ip in eval(ips.content):
        list.append(ip[0]+':'+str(ip[1]))
        print list
    return list

GetIps()