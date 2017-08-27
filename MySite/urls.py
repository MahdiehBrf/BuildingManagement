from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^resident/', include('Resident.urls', namespace="resident")),
    url(r'^manager/', include('Manager.urls', namespace="manager")),
    url(r'^$', views.index, name='index'),
    url(r'^send_feedback/$', views.send_feedback,name='send_feedback'),
    url(r'^logout/$', views.logout, name='log_out'),
    url(r'^forget_password/$', views.forget_password, name='forget_password'),
]
