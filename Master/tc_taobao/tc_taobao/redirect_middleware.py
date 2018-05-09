#-*-coding:utf-8-*-
from scrapy.exceptions import IgnoreRequest

from util.message import sendMessage_warning

#过滤器，将可以访问的发送给下载器，如果有一个其他状态码例如重定向的，就直接发送，不用重新访问tcp，这会节省耗能


class Redirect_Middleware():

    global count
    count = 1
    def process_response(self,request,response,spider):
        #处理下载完成的response
        #排除重定向
        http_code = response.status
        if http_code // 100 == 3 and http_code != 304:
            global count
            if count == 1:
                sendMessage_warning()
            count += 1
            return request.replace(dont_filter=True)
        #400是无权访问，就丢弃这个
        if http_code // 100 == 4:
            raise IgnoreRequest(u'404')
        if http_code // 100 == 5:
            return request.replace(dont_filter=True)
