from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view_bills/$', views.view_bills, name='viewBills'),
    url(r'^calculate_receipts/$', views.calculate_receipts, name='calculateReceipts'),
    url(r'^(?P<reserve_id>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.[0-9]*\W\d{2}:\d{2})/reject_reserve/$', views.reject_reserve,
        name='reject_reserve'),
    url(r'^(?P<reserve_id>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.[0-9]*\W\d{2}:\d{2})/accept_reserve/$', views.accept_reserve, name='accept_reserve'),
    url(r'^(?P<request_id>[0-9]+)/view_request/$', views.view_request, name='viewRequest'),
    url(r'^(?P<request_id>[0-9]+)/delete_request/$', views.delete_request, name='delete_request'),
    url(r'^select_contact/$', views.select_contact, name='select_contact'),
    url(r'^message/$', views.message, name='message'),
    url(r'^(?P<neighbour_id>[0-9]+)/edit_n/$', views.edit_n, name='editN'),
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
    url(r'^events/$', views.view_event, name='events'),
    url(r'^enterBill/$', views.enter_bill, name='enterBill'),
    url(r'^(?P<unit_id>[0-9]+)/delete_unit/$', views.delete_unit, name='deleteUnit'),
    url(r'^(?P<neighbour_id>[0-9]+)/delete_neighbour/$', views.delete_neighbour, name='deleteNeighbour'),
    url(r'^$', views.account, name='account'),
    url(r'^add_facility/$', views.add_facility, name='addFacility'),
    url(r'^edit_facility/$', views.edit_facility, name='editFacility'),
    url(r'^(?P<facility_id>[0-9]+)/delete_facility/$', views.delete_facility, name='deleteFacility'),
    ]
