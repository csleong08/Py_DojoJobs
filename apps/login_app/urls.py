from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dash$', views.dash),
    url(r'^addJob$', views.addJob),
    url(r'^createJob$', views.createJob),
    url(r'^delete$', views.delete),
    url(r'^add/(?P<job_id>\d+)/(?P<user_id>\d+)$', views.add),
    url(r'^view/(?P<job_id>\d+)$', views.view),
    url(r'^edit/(?P<job_id>\d+)$', views.edit),
    url(r'^update/(?P<job_id>\d+)$', views.update),
]