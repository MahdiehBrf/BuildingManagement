from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^select_contact/$', views.select_contact, name='select_contact'),
    url(r'^message/$', views.message, name='message'),
    url(r'^reserves/$', views.view_reserves, name='myReserves'),
    url(r'^reserve/$', views.reserve, name='reserve'),
    url(r'^(?P<receipt_id>[0-9]+)/select_payWay/$', views.select_pay_way, name='select_payWay'),
    url(r'^(?P<receipt_id>[0-9]+)/view_bill/$', views.view_bill, name='viewBill'),
    url(r'^bills/$', views.view_bills, name='bills'),
    url(r'^paying_reports/$', views.paying_reports, name='payingReports_user'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^board/$', views.view_board, name='board'),
    url(r'^events/$', views.view_event, name='events'),
    url(r'^increase/$', views.increase_cash, name='increase'),
    url(r'^$', views.account, name='account'),
    ]
