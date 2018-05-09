from django.conf.urls import url

from message import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^assignment/$', views.assignment, name='assignment'),
    url(r'^crawl/$', views.crawl, name='crawl'),
    url(r'^cloudmusic/$', views.cloudMusic, name='cloudmusic'),
    url(r'^feedback/$', views.feedback, name='feedback'),
]