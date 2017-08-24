from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^select_contact/$', views.select_contact, name='select_contact'),
    url(r'^message/$', views.message, name='message'),
    url(r'^reserves/$', views.view_reserves, name='myReserves'),
    url(r'^reserve/$', views.reserve, name='reserve'),
    url(r'^view_bill/$', views.view_bill, name='viewBill'),
    url(r'^bills/$', views.view_bills, name='bills'),
    url(r'^paying_reports/$', views.paying_reports, name='payingReports_user'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^board/$', views.view_board, name='board'),
    url(r'^$', views.account, name='account'),
    ]
