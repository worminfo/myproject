from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<process>.+)/(?P<user_id>[0-9]+)$', views.modify, name='modify'),
    # url(r'^login/$', views.login, name='login'),
    # url(r'^$', views.generate_report, name='index')
    url(r'^$', views.calendar_list, name='index'),
    url(r'^add/$', views.add_event, name='add_timetable'),
    
]
