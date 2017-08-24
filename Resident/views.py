from django.shortcuts import render

# Create your views here.


def account(request):
    return render(request, 'resident/account.html')


def view_board(request):
    return render(request, 'resident/board.html')


def edit_profile(request):
    return render(request, 'resident/edit_profile.html')


def paying_reports(request):
    return render(request, 'resident/payingReports_user.html')


def reserve(request):
    return render(request, 'resident/reserve.html')


def message(request):
    return render(request, 'resident/message.html')


def select_contact(request):
    return render(request, 'resident/select_contact.html')


def view_bills(request):
    return render(request, 'resident/bills.html')


def view_reserves(request):
    return render(request, 'resident/myReserves.html')


def view_bill(request):
    return render(request, 'resident/viewBill.html')