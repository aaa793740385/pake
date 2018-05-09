# _*_ encoding:utf-8 _*_
"""djangostart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from message.views import LoginView, logout, reviseKey, startCrawl, taskDetail, musicCrawl, signMap, excelOutput, \
    excelProcess, priceRange, submitFeedback

urlpatterns = {
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^', include('message.urls', namespace='index')),
    url(r'^logout/$', logout, name="logout"),
    url(r'^revisekey/$', reviseKey, name="reviseKey"),
    url(r'^startCrawl/$', startCrawl, name='startCrawl'),
    url(r'^taskDetail/$', taskDetail, name='taskDetail'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': 'media/'}),
    url(r'^musicCrawl/$', musicCrawl, name='musicCrawl'),
    url(r'^signMap/$', signMap, name='signMap'),
    url(r'^excelOutput/$', excelOutput, name='excelOutput'),
    url(r'^excelProcess/$', excelProcess, name='excelProcess'),
    url(r'^priceRange/$', priceRange, name='priceRange'),
    url(r'^submitFeedback/$', submitFeedback, name='submitFeedback'),



    # url(r'^register/$', RegisterView.as_view(), name = "register"),#注册页面
    # url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    # url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="reset_pwd"),
    # url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd")#验证链接
}
