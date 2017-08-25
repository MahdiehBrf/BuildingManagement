from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from MySite.forms import DisplayForm
from MySite.models import News, Event, Unit, Facility
from Resident.forms import ReserveForm, DateForm
from Resident.models import PayByAccount, Resident, Reserve
from Resident.models import PayByBank


def account(request):
    return render(request, 'resident/account.html')


@login_required
def view_board(request):
    resident = request.user.member.resident
    events = None
    news_set = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            news_set = resident.unit.block.board.news_set.filter(board__block=resident.unit.block, date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
            events = resident.unit.block.board.event_set.filter(board__block=resident.unit.block, date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
        else:
            news_set = resident.unit.block.board.news_set.all()
            events = resident.unit.block.board.event_set.all()
        if request.POST['choose'] == 'جدیدترین':
            news_set = news_set.order_by('-date')
            events = events.order_by('-date')
    else:
        news_set = resident.unit.block.board.news_set.all()
        events = resident.unit.block.board.event_set.all()
    return render(request, 'resident/board.html', {'events': events, 'newsSet': news_set})


def edit_profile(request):
    return render(request, 'resident/edit_profile.html')


def paying_reports(request):
    resident = request.user.member.resident
    bank_reports = None
    account_reports = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            bank_reports = PayByBank.objects.filter(resident=resident,
                                                    date__gte=form.cleaned_data['startDate'],
                                                    date__lte=form.cleaned_data['finishDate'])
            account_reports = PayByAccount.objects.filter(account__resident=resident,
                                                          date__gte=form.cleaned_data['startDate'],
                                                          date__lte=form.cleaned_data['finishDate'])
        else:
            bank_reports = PayByBank.objects.filter(resident=resident)
            account_reports = PayByAccount.objects.filter(account__resident=resident)
        if request.POST['choose'] == 'جدیدترین':
            bank_reports = bank_reports.order_by('-date')
            account_reports = account_reports.order_by('-date')
    else:
        bank_reports = PayByBank.objects.filter(resident=resident)
        account_reports = PayByAccount.objects.filter(account__resident=resident)
    return render(request, 'resident/payingReports_user.html',
                  {'account_reports': account_reports, 'bank_reports': bank_reports})


def reserve(request):
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        dateForm = DateForm(request.POST)
        if form.is_valid() and dateForm.is_valid():
            resident_reserve = Reserve()
            resident_reserve.facility = form.cleaned_data['facility']
            resident_reserve.use_startDate = datetime.combine(dateForm.cleaned_data['use_startDate_0'],dateForm.cleaned_data['use_startDate_1'])
            resident_reserve.use_finishDate = datetime.combine(dateForm.cleaned_data['use_finishDate_0'],dateForm.cleaned_data['use_finishDate_1'])
            resident_reserve.reserve_date = datetime.now()
            resident_reserve.state = 'NC'
            resident_reserve.resident = request.user.member.resident
            resident_reserve.cost = resident_reserve.facility.cost
            resident_reserve.save()
            return HttpResponseRedirect(reverse('site:resident:myReserves'))
    else:
        form = ReserveForm()
    return render(request, 'resident/reserve.html', {'form': form})


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