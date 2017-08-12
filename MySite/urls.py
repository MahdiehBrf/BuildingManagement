from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^manager/', include('Manager.urls', namespace="manager")),
    url(r'^$', views.index, name='index'),
    url(r'^manager/', views.send_feedback,name='send_feedback'),
]