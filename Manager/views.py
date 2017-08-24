from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from Manager.forms import RequestForm, MessageForm
from Manager.models import Request
from MySite.forms import EventForm, NewsForm, DisplayForm, ComplexForm
from MySite.models import Event, News, Unit
from MyUser.forms import SignupForm1
from MyUser.models import Member, Message
from Resident.forms import ResidentForm
from Resident.models import Reserve, PayByBank, PayByAccount


@login_required
def account(request):
    return render(request, 'manager/account.html')


@login_required
def add_to_board(request):
    if request.method == 'POST':
        if request.POST['choose'] == 'event':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.date = datetime.now().date()
                event.save()
        else:
            form = NewsForm(request.POST)
            if form.is_valid():
                news = form.save(commit=False)
                news.date = datetime.now().date()
                news.save()
        return HttpResponseRedirect(reverse('site:manager:board'))
    else:
        form = EventForm()
    return render(request, 'manager/add_to_board.html', {'form': form})


@login_required
def view_board(request):
    manager = request.user.member.manager
    events = None
    news_set = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            news_set = News.objects.filter(board__block__complex=manager.complex, date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
            events = Event.objects.filter(board__block__complex=manager.complex, date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
        else:
            news_set = News.objects.filter(board__block__complex=manager.complex)
            events = Event.objects.filter(board__block__complex=manager.complex)
        if request.POST['choose'] == 'جدیدترین':
            news_set = news_set.order_by('-date')
            events = events.order_by('-date')
    else:
        news_set = News.objects.filter(board__block__complex=manager.complex)
        events = Event.objects.filter(board__block__complex=manager.complex)
    return render(request, 'manager/board.html', {'events': events, 'newsSet': news_set})



@login_required
def edit_profile(request):
    user = request.user
    user_form = SignupForm1(instance = user)
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = SignupForm1(request.POST, instance=request.user)
            member = Member.objects.get(user=request.user)
            if user_form.is_valid():
                user_form.save()
                member.user = request.user
                member.phone_number = request.POST.get('phone_number')
                member.save()
                return HttpResponseRedirect(reverse('site:manager:add_neighbour'))
    return render(request, 'manager/edit_profile.html', {'user': user, 'form': user_form})


@login_required
def edit_complex_information(request):
    if request.method == 'POST':
        form = ComplexForm(request.POST)
        if form.is_valid():
            complex = form.save(commit=False)
            complex.manager = Member.objects.filter(user=request.user)[0].manager
            complex.save()
            return HttpResponseRedirect(reverse('site:manager:add_neighbour'))
    else:
        form = ComplexForm()
    print(form)
    return render(request, 'manager/edit_complex_information.html', {'form': form})


@login_required
def edit_neighbours(request):
    return render(request, 'manager/editNeighbours.html')


@login_required
def edit_unit(request):
    return render(request, 'manager/editUnit.html')

@login_required
def paying_reports(request):
        manager = request.user.member.manager
        bank_reports = None
        account_reports = None
        unit = None
        if request.method == 'POST':
            form = DisplayForm(request.POST)
            if form.is_valid():
                bank_reports = PayByBank.objects.filter(resident__unit__block__complex__manager=manager, date__gte=form.cleaned_data['startDate'],
                                               date__lte=form.cleaned_data['finishDate'])
                account_reports = PayByAccount.objects.filter(resident__unit__block__complex__manager=manager, date__gte=form.cleaned_data['startDate'],
                                              date__lte=form.cleaned_data['finishDate'])
            else:
                bank_reports = PayByBank.objects.filter(resident__unit__block__complex__manager=manager)
                account_reports = PayByAccount.objects.filter(account__resident__unit__block__complex__manager=manager)
            if request.POST['choose'] == 'جدیدترین':
                bank_reports = bank_reports.order_by('-date')
                account_reports = account_reports.order_by('-date')
            if request.POST['unit']:
                unit_set = Unit.objects.filter(id=request.POST['unit'])
                if unit_set:
                    unit = unit_set[0]
                    resident = unit.resident
                    resident_account = resident.account
                    bank_reports = bank_reports.filter(resident=resident)
                    account_reports = account_reports.filter(account=resident_account)
        else:
            bank_reports = PayByBank.objects.filter(resident__unit__block__complex__manager=manager)
            account_reports = PayByAccount.objects.filter(account__resident__unit__block__complex__manager=manager)
        return render(request, 'manager/payingReports.html', {'account_reports': account_reports, 'bank_reports': bank_reports})


@login_required
def reserves_check(request):
    reserves = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            reserves = Reserve.objects.filter(reserve_date__gte=form.cleaned_data['startDate'],
                                              reserve_date__lte=form.cleaned_data['finishDate'])#  TODO
        else:
            reserves = Reserve.objects.all()
        if request.POST['choose'] == 'جدیدترین':
            reserves = reserves.order_by('-reserve_date')
    else:
        reserves = Reserve.objects.all()
    return render(request, 'manager/reservesCheck.html', {'reserves': reserves})


@login_required
def accept_reserve(request, reserve_id):
    reserve = get_object_or_404(Reserve, pk=reserve_id)
    reserve.state = 'A'
    reserve.save()
    return HttpResponseRedirect(reverse('site:manager:reservesCheck'))


@login_required
def requests(request):
    manager_requests = None
    if request.method == 'POST':
        # manager_requests = Request.objects.all()
        manager_requests = request.user.member.manager.request_set.all()
        if request.POST['choose'] == 'W':
            manager_requests = manager_requests.filter(state='W')
        elif request.POST['choose'] == 'C':
            manager_requests = manager_requests.filter(state='C')
    else:
        manager_requests = Request.objects.all()
    return render(request, 'manager/requests.html', {'requests': manager_requests})

'''
    member = models.OneToOneField(User)
    member_count = models.IntegerField()
    car_count = models.IntegerField()
    unit = models.OneToOneField(Unit)p
'''
@login_required
def add_neighbour(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            manager_request = form.save(commit=False)
            manager_request.manager = Member.objects.filter(user= request.user)[0].manager
            manager_request.state = 'W'
            manager_request.save()
        return HttpResponseRedirect(reverse('site:manager:requests'))
    else:
        form = ResidentForm()
    return render(request, 'manager/addRequest.html', {'form': form})
    #return render(request, 'addNeighbour.html')


@login_required
def add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            manager_request = form.save(commit=False)
            manager_request.manager = Member.objects.filter(user= request.user)[0].manager
            manager_request.state = 'W'
            manager_request.save()
        return HttpResponseRedirect(reverse('site:manager:requests'))
    else:
        form = RequestForm()
    return render(request, 'manager/addRequest.html', {'form': form})


@login_required
def add_unit(request):
    return render(request, 'manager/addUnit.html')


@login_required
def edit_n(request):
    return render(request, 'manager/editN.html')


@login_required
def select_contact(request):
    s = Member.objects.get(user=request.user)
    ms = Message.objects.filter(Q(sender=s) | Q(receiver=s))
    return render(request, 'manager/select_contact.html', {'messages': ms})


@login_required
def message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.sender = Member.objects.get(user=request.user)
            m.theme_type = 0
            m.save()
        return HttpResponseRedirect(reverse('site:manager:select_contact'))
    else:
        form = MessageForm()
    return render(request, 'manager/message.html', {'form': form})


@login_required
def view_request(request, request_id):
    manager_request = get_object_or_404(Request, pk=request_id)
    return render(request, 'manager/viewRequest.html', {'request': manager_request})

@login_required
def delete_request(request, request_id):
    manager_request = get_object_or_404(Request, pk=request_id)
    manager_request.delete()
    return HttpResponseRedirect(reverse('site:manager:requests'))