from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^(?P<reserve_id>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.[0-9]*\W\d{2}:\d{2})/$', views.accept_reserve, name='accept_reserve'),
    url(r'^(?P<request_id>[0-9]+)/view_request/$', views.view_request, name='viewRequest'),
    url(r'^(?P<request_id>[0-9]+)/delete_request/$', views.delete_request, name='delete_request'),
    url(r'^select_contact/$', views.select_contact, name='select_contact'),
    url(r'^message/$', views.message, name='message'),
    url(r'^edit_n/$', views.edit_n, name='editN'),
    url(r'^add_unit/$', views.add_unit, name='addUnit'),
    url(r'^add_request/$', views.add_request, name='addRequest'),
    url(r'^add_neighbour/$', views.add_neighbour, name='addNeighbour'),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^reserves_check/$', views.reserves_check, name='reservesCheck'),
    url(r'^paying_reports/$', views.paying_reports, name='payingReports'),
    url(r'^edit_unit/$', views.edit_unit, name='editUnit'),
    url(r'^edit_neighbours/$', views.edit_neighbours, name='editNeighbours'),
    url(r'^edit_complex_information/$', views.edit_complex_information, name='edit_complex_information'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^board/add_to_board$', views.add_to_board, name='add_to_board'),
    url(r'^board/$', views.view_board, name='board'),
    url(r'^enterBill/$', views.enter_bill, name='enterBill'),
    url(r'^$', views.account, name='account'),
    ]
