from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    # url(r'^(?P<process>.+)/(?P<user_id>[0-9]+)$', views.modify, name='modify'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^delete/$', views.remove_user, name='remove_user'),
    url(r'^add/$', views.add_user, name='add_user'),

    url(r'^modify/$', views.modify_user, name='modify_user'),
    url(r'^modify/(?P<username>.+)/$', views.modify_user, name='modify_user'),
    url(r'^$', views.list_user, name='list_user'),

    url(r'^class/$', views.list_class, name='list_class'),
    url(r'^class/add/$', views.create_class, name='create_class'),
    url(r'^class/add/(?P<class_code>.+)/$', views.add_classmember, name='add_classmember'),
    url(r'^class/modify/(?P<class_code>.+)/$', views.modify_class, name='modify_class'),
    url(r'^class/modify/(?P<class_code>.+)/(?P<user_id>[0-9]+)/classno$', views.modify_classnumber, name='modify_classnumber'),
    url(r'^class/delete/(?P<class_code>.+)/(?P<user_id>[0-9]+)/$', views.remove_classmember, name='remove_classmember'),    
    url(r'^class/delete/(?P<class_code>.+)/$', views.delete_class, name='delete_class'),

    url(r'^(?P<username>.+)/$', views.view_user, name='view_user'),
]