from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^board/add_to_board$', views.add_to_board, name='add_to_board'),
    url(r'^board/$', views.view_board, name='board'),
    url(r'^$', views.account, name='account'),
    ]
