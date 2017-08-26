from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from MySite.forms import DisplayForm
from MyUser.models import Member, Message
from Resident.forms import ReserveForm, DateForm, MessageForm
from Resident.models import PayByAccount, Reserve, Receipt
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
        elif request.POST['choose'] == 'قدیمی ترین':
            news_set = news_set.order_by('date')
            events = events.order_by('date')
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
        elif request.POST['choose'] == 'قدیمی ترین':
            bank_reports = bank_reports.order_by('date')
            account_reports = account_reports.order_by('date')
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


@login_required
def message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.sender = Member.objects.get(user=request.user)
            m.theme_type = 0
            m.save()
        return HttpResponseRedirect(reverse('site:resident:select_contact'))
    else:
        form = MessageForm()
    return render(request, 'resident/message.html', {'form': form})


@login_required
def select_contact(request):
    s = Member.objects.get(user=request.user)
    ms = Message.objects.filter(Q(sender=s) | Q(receiver=s))
    return render(request, 'resident/select_contact.html', {'messages': ms})


def view_bills(request):
    resident = request.user.member.resident
    receipts = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            receipts = Receipt.objects.filter(state='NP', resident=resident, start_date__gte=form.cleaned_data['startDate'],
                                              start_date__lte=form.cleaned_data['finishDate'])  # TODO
        else:
            receipts = Receipt.objects.filter(state='NP', resident=resident)
        if request.POST['choose'] == 'جدیدترین':
            receipts = receipts.order_by('-start_date')
        elif request.POST['choose'] == 'قدیمی ترین':
            receipts = receipts.order_by('start_date')
    else:
        receipts = Receipt.objects.filter(state='NP', resident=resident)
    return render(request, 'resident/bills.html', {'receipts': receipts})


def view_reserves(request):
    resident = request.user.member.resident
    reserves = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            reserves = Reserve.objects.filter(resident=resident, reserve_date__gte=form.cleaned_data['startDate'],
                                              reserve_date__lte=form.cleaned_data['finishDate'])  # TODO
        else:
            reserves = Reserve.objects.filter(resident=resident)
        if request.POST['choose'] == 'جدیدترین':
            reserves = reserves.order_by('-reserve_date')
        elif request.POST['choose'] == 'قدیمی ترین':
            reserves = reserves.order_by('reserve_date')
    else:
        reserves = Reserve.objects.filter(resident=resident)
    return render(request, 'resident/myReserves.html', {'reserves': reserves})


def view_bill(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)
    block = receipt.resident.unit.block
    size = 0
    events = block.board.event_set.filter(date__gt=receipt.start_date, date__lte=receipt.finish_date)
    bills= block.bill_set.filter(date__gt=receipt.start_date, date__lte=receipt.finish_date)
    reserves = receipt.resident.reserve_set.filter(reserve_date__gt=receipt.start_date, reserve_date__lte=receipt.finish_date, state='A')
    for unit in block.unit_set.all():
        if unit.resident:
            size += unit.resident.member_count
    eventsCost = []
    for event in events:
        eventsCost.append(round(event.cost*receipt.resident.member_count/size, 4))
    billsCost = []
    for bill in bills:
        billsCost.append(round(bill.cost*receipt.resident.member_count/size, 4))
    return render(request, 'resident/viewBill.html', {'receipt': receipt, 'events': zip(events, eventsCost),'bills': zip(bills, billsCost), 'reserves':reserves, 'size':size})


def pay_receipt(request, receipt_id):
    return render(request, 'resident/viewBill.html')