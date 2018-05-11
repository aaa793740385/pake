# -*- coding:utf-8 -*-
from datetime import datetime

import sys
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.views.generic.base import View
from pymongo import MongoClient
import json
# from django.contrib.auth.hashers import make_password
# from .forms import LoginForm, RegisterForm, ModifyPwdForm, ForgetForm
# from django.contrib.auth.decorators import login_required
# from .models import UserProfile,EmailVerifyRecord
# from utils.email_send import send_register_email
# from .models import UserMessage
from NEMCrawler.NEM_spider import startCrawlMusic
from message import models
from utils import InsertRedis
from utils.ExcelService import outputExcel, readFile
from utils.mapService import mapMaking
from utils.priceService import pricePieMaking

reload(sys)
sys.setdefaultencoding('utf-8')
conn = MongoClient('localhost', 27017)
db = conn.crawlData


class LoginView(View):
    def get(self, request):
        return render(request, "home.html")

    def post(self, request):
        user_name = request.POST.get("username")  # 这里是superuser和密码
        pass_word = request.POST.get("password")
        user = auth.authenticate(username=user_name, password=pass_word)  # 这里验证的是superuser的账号和密码一开始
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse('success_login')
            else:
                return HttpResponse('not_activated')
        else:
            return HttpResponse('error')

    pass


def home(request):
    return render(request, 'home.html')


def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    auth.logout(request)
    return HttpResponseRedirect('/')


def personal(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    id = request.user.id
    # models.UserInformation.objects.create(id=id)  #进入个人中心报错请去掉注释，成功进去后再重新注释
    tasks = models.Task.objects.filter(user=request.user.id)
    task_ids = []
    for i in tasks:
        task_ids.append(str(i.id))
    my_getDetail = db.taobao
    detail_total = my_getDetail.find({"task_id": {"$in": task_ids}}).count()
    task_total = len(task_ids)
    information = models.UserInformation.objects.get(pk=id)
    return render(request, 'personal.html',
                  {"inf": information, "task_total": task_total, "detail_total": detail_total})


def reviseKey(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.is_ajax():
        newpassword = request.POST.get('password')
        u = User.objects.get(username=request.user.username)
        u.set_password(newpassword)
        u.save()
        return HttpResponse('success')


def assignment(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    list = models.Task.objects.filter(user=request.user.id)
    list = list[::-1]
    paginator = Paginator(list, 10, 2)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'assignment.html', {"list": tasks})


def crawl(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request, 'crawl.html')


def startCrawl(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.is_ajax():
        import time
        oldtime = models.UserInformation.objects.get(pk=request.user.id).crawl_time
        newtime = time.mktime(datetime.now().timetuple())
        print(float(newtime)-float(oldtime))
        if float(newtime)-float(oldtime) >= 300:
            name = str(request.GET.get('name'))
            general = str(request.GET.get('general'))
            remark = str(request.GET.get('remark'))
            createTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            models.Task.objects.create(user=request.user.id, name=name, general=general, remark=remark, time=createTime)
            task = models.Task.objects.latest('id')
            InsertRedis.inserintotc("http://taobao.com/", 1, task)
            user = models.UserInformation.objects.get(pk=request.user.id)
            user.crawl_time = str(newtime)
            user.save()
            return HttpResponse('success')
        else:
            return HttpResponse('limited time')


def taskDetail(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.is_ajax():
        my_getDetail = db.taobao
        taskId = request.POST.get('id')
        detail = my_getDetail.find({"task_id": str(taskId)})
        list = []
        for i in detail:
            del i[u'_id']
            list.append(i)
        # list = [dict(t) for t in set([tuple(d.items()) for d in list])]  # 去重功能
        return HttpResponse(json.dumps(list), content_type="application/json")


def cloudMusic(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request, 'cloudMusic.html')


def feedback(request):
    return render(request, 'feedBack.html')


def musicCrawl(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    star_id = request.GET.get('star_id')
    startCrawlMusic(star_id, request.user.id)
    return HttpResponse('success')


def signMap(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.is_ajax():
        task_id = request.GET.get("task_id")
        mapMaking(task_id)
        return HttpResponse('success')


def excelProcess(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    task_id = request.GET.get("task_id")
    outputExcel(task_id)
    return HttpResponse('success')


def excelOutput(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    the_file_name = 'crawl.xls'  # 显示在弹出对话框中的默认的下载文件名
    filename = 'downloads/excel/crawl' + request.GET.get("task_id") + '.xls'  # 要下载的文件路径
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def priceRange(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    task_id = request.GET.get("task_id")
    start_range = request.GET.get("start_range")
    end_range = request.GET.get("end_range")
    pricePieMaking(task_id, start_range, end_range)
    return HttpResponse('success')


def submitFeedback(request):
    content = request.GET.get('content')
    models.Feedback.objects.create(content=content)
    return HttpResponse('success')


# #注册响应的页面
# class RegisterView(View):
#     def get(self,request):
#         return render(request, "register.html")#显示的htmlurl
#     def post(self,request):
#         register_form = RegisterForm(request.POST)  # 加入前端传进来的参数
#         if register_form.is_valid():
#             user_name = request.POST.get("email", "")   #email验证
#             pass_word = request.POST.get("password", "")
#
#             user_profile = UserProfile()#实例化一个对象
#             # 这里将邮箱作为username，因为数据库中username是必填的，然而邮箱它有进行@这种格式的判断，所以后面用邮箱登录进去
#             user_profile.username = user_name
#             user_profile.email = user_name
#             user_profile.is_active = False
#             #对密码进行加密，再保存
#             user_profile.password = make_password(pass_word)
#             user_profile.save()#保存改账号密码到数据库
#
#             send_register_email(user_name,"register")#验证字符串
#             #判断是否注册成功，如果注册成功，返回login的页面
#             return render(request, "login.html")
#         else:
#             return render(request, "register.html",{"register_form":register_form})
#
# #修改密码
# class ModifyPwdView(View):
#     def post(self,request):
#         modify_form = ModifyPwdForm(request.POST)
#         if modify_form.is_valid():
#             pwd1 = request.POST.get("password1","")
#             pwd2 = request.POST.get("password2","")
#             email = request.POST.get("email","")
#             if pwd1 != pwd2:
#                 return render(request,"password_reset.html",{"email":email,"msg":"密码不一致"})
#             user = UserProfile.objects.get(email = email)
#
#             user.password = make_password(pwd2)
#             user.save()
#             return render(request,"login.html")     #修改密码成功，返回登录页面
#         else:
#             email = request.POST.get("email","")
#             return render(request,"password_reset.html")
#
# #忘记密码
# class ForgetPwdView(View):
#     def get(self,request):
#         return render(request,"forgetpwd.html")
#     def post(self,request):
#         forget_form = ForgetForm(request.POST)#判断这个form是否合法
#         if forget_form.is_valid():
#             email = request.POST.get("email","")
#             send_register_email(email, "forget")
#             return render(request,"send_success.html")
#         else:
#             return render(request, "forgetpwd.html")
#
# class ActiveUserView(View):
#     def get(self,request,active_code):
#         #查询记录是否存在
#         all_records = EmailVerifyRecord.objects.filter(code = active_code)  #查询在数据库中满足这个条件的实例
#         if all_records: #有这个实例
#             for record in all_records:  #将实例遍历出来
#                 email = record.email    #提取出来改email
#                 user = UserProfile.objects.get(email = email)   #查询满足email通的实例在UserProfile中
#                 user.is_active = True   #激活
#                 user.save() #保存
#         else:
#             return render(request,"active_fail.html")
#         return render(request,"login.html")
#
#
