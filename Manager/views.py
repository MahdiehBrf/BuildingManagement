import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from Manager.forms import RequestForm, MessageForm, BillForm
from Manager.models import Request
from MySite.forms import EventForm, NewsForm, DisplayForm, ComplexForm
from MySite.models import Event, News, Unit, Block, Board
from MySite.models import Facility
from MyUser.forms import SignupForm1
from MyUser.forms import SignupForm2
from MyUser.models import Member, Message
from Resident.forms import ResidentForm
from Resident.models import Reserve, PayByBank, PayByAccount, Receipt
from Resident.models import Resident


@login_required
# the first page that manager see after login
def account(request):
    return render(request, 'manager/payingReports.html')


@login_required
# when manager click on the "add to board" in board page, a form to create event will be shown and manager can choose to
# create event or news, after clicking on "record" base on which manager chose an event or news will be created with
# date of today. then page will be redirected to board page to view all the event and news he created
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
# when manager click on "news" in the menu, he can see a table include of news of all block of that complex with theirs
# attributes
# can select a period to see news in that period
# can select an order of seeing news
def view_board(request):
    manager = request.user.member.manager
    events = None
    news_set = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            news_set = News.objects.filter(board__block__complex=manager.complex,
                                           date__range=[form.cleaned_data['startDate'],
                                                        form.cleaned_data['finishDate']])
            events = Event.objects.filter(board__block__complex=manager.complex,
                                          date__range=[form.cleaned_data['startDate'], form.cleaned_data['finishDate']])
        else:
            news_set = News.objects.filter(board__block__complex=manager.complex)
            events = Event.objects.filter(board__block__complex=manager.complex)
        if request.POST['choose'] == 'جدیدترین':
            news_set = news_set.order_by('-date')
            events = events.order_by('-date')
        elif request.POST['choose'] == 'قدیمی ترین':
            news_set = news_set.order_by('date')
            events = events.order_by('date')
    else:
        news_set = News.objects.filter(board__block__complex=manager.complex)
        events = Event.objects.filter(board__block__complex=manager.complex)
    return render(request, 'manager/board.html', {'events': events, 'newsSet': news_set})


@login_required
# when manager click on "events" in the menu, he can see a table include of events of all block of that complex with
#  theirs attributes
# can select a period to see events in that period
# can select an order of seeing news
def view_event(request):
    manager = request.user.member.manager
    events = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            events = Event.objects.filter(board__block__complex=manager.complex,
                                          date__range=[form.cleaned_data['startDate'], form.cleaned_data['finishDate']])
        else:
            events = Event.objects.filter(board__block__complex=manager.complex)
        if request.POST['choose'] == 'جدیدترین':
            events = events.order_by('-date')
    else:
        events = Event.objects.filter(board__block__complex=manager.complex)
    return render(request, 'manager/events.html', {'events': events})


@login_required
def edit_profile(request):
    """
    This function is for editting manager profile. With this section, manager can get his previeus profile and change them.
    :param request: Contain manager id for getting its information and Updating them.
    :return: After entering information, if there is not any fault in filling field, return to main page of manager site.
    """
    user = request.user
    user_form = SignupForm1(instance=user)
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = SignupForm1(request.POST, instance=request.user)
            member = Member.objects.get(user=request.user)
            if user_form.is_valid():
                user_form.save()
                member.user = request.user
                member.phone_number = request.POST.get('phone_number')
                member.save()
                return HttpResponseRedirect(reverse('site:manager:account'))
    return render(request, 'manager/edit_profile.html', {'user': user, 'form': user_form})


@login_required
def edit_complex_information(request):
    """
    with this function manager can edit his complex information like name, address and number of blocks inside complex and also number of unit inside each block in complex.
    :param request: This passed field contain manager id and also complex id for getting its previuos informatoin. and also contains data filled by manager for editing previeus complex information
    :return: After filling required field, if there is no fault in entering data, opens main page of manager's site.
    """
    if request.method == 'POST':
        form = ComplexForm(request.POST, instance=request.user.member.manager.complex)
        blockNum = int(request.POST.get('blockNum'))
        if form.is_valid():
            complex = form.save(commit=False)
            complex.manager = Member.objects.filter(user=request.user)[0].manager
            complex.save()
            blocks = Block.objects.filter(complex=complex)
            s = len(blocks)
            if int(blockNum) < s:
                for i in range(s - blockNum):
                    blocks[i].delete()
            elif int(blockNum) > s:
                for i in range(int(blockNum) - s):
                    block = Block.objects.create(complex=complex)
                    board = Board.objects.create(block=block)
                    block.save()
                    board.save()
            return HttpResponseRedirect(reverse('site:manager:account'))
    else:
        form = ComplexForm(instance=request.user.member.manager.complex)
        blocks = Block.objects.filter(complex=form.instance)
        blockNum = len(blocks)
    return render(request, 'manager/edit_complex_information.html',
                  {'form': form.initial, 'blockNum': blockNum})


@login_required
def edit_neighbours(request):
    """
    With this function, manager can see neighbours for his complex.
    :param request: request contains manager id and complex id for getting resident that their complex is equal to this manager's complex.
    :return:As a result of this function, manager can see a html page with his complex's neighbours and their information like number of car, number of family member and their block number.
    """
    complex = request.user.member.manager.complex
    neighbours = Resident.objects.filter(unit__block__complex=complex)
    return render(request, 'manager/editNeighbours.html', {'neighbours': neighbours})


@login_required
def delete_neighbour(request,neighbour_id):
    """
    This function is for deleting special neighbour.
    :param request:
    :param neighbour_id: It is id of the neighbour, we want to delete it
    :return:This function result is deleting selected neighbour and returning and opening a page that shows all neighbours to managers
    """
    Resident.objects.get(id=neighbour_id).delete()
    return HttpResponseRedirect(reverse('site:manager:editNeighbours'))


@login_required
def edit_unit(request):
    '''
    This function is for getting all units belonging to this managers complex and thier data and showing them to the manager
    :param request: We can get manager id  and also complex id
    :return: As a result of this function, A page containing units and their informatoin is displayed.
    '''
    complex = request.user.member.manager.complex
    units = Unit.objects.filter(block__complex=complex)
    return render(request, 'manager/editUnit.html', {'units': units})


@login_required
# when manager click on "resident's paying reports" in the menu, he can see a table include of all paying reports of
#  all residents in all block of that complex with theirs attributes
# can select a period to see reports in that period
# can select an order of seeing reports
# can select a unit to see reports of that unit
def paying_reports(request):
        manager = request.user.member.manager
        bank_reports = None
        account_reports = None
        unit = None
        if request.method == 'POST':
            form = DisplayForm(request.POST)
            if form.is_valid():
                bank_reports = PayByBank.objects.filter(resident__unit__block__complex__manager=manager,
                                                        date__range=[form.cleaned_data['startDate'],
                                                                     form.cleaned_data['finishDate']])
                account_reports = PayByAccount.objects.filter(resident__unit__block__complex__manager=manager,
                                                              date__range=[form.cleaned_data['startDate'],
                                                                           form.cleaned_data['finishDate']])
            else:
                bank_reports = PayByBank.objects.filter(resident__unit__block__complex__manager=manager)
                account_reports = PayByAccount.objects.filter(account__resident__unit__block__complex__manager=manager)
            if request.POST['choose'] == 'جدیدترین':
                bank_reports = bank_reports.order_by('-date')
                account_reports = account_reports.order_by('-date')
            elif request.POST['choose'] == 'قدیمی ترین':
                bank_reports = bank_reports.order_by('date')
                account_reports = account_reports.order_by('date')
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
        return render(request, 'manager/payingReports.html', {'account_reports': account_reports,
                                                              'bank_reports': bank_reports})


@login_required
# when manager click on "reserves requests" in the menu, he can see a table include of all reserve requests of
#  all residents in all block of that complex with theirs attributes
# can select a period to see reserves in that period
# can select an order of seeing reserves
# can choose to accept or reject an unchecked request and trigger the state of others
def reserves_check(request):
    manager = request.user.member.manager
    reserves = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            reserves = Reserve.objects.filter(resident__unit__block__complex__manager=manager,
                                              reserve_daterange=[form.cleaned_data['startDate'],
                                                                 form.cleaned_data['finishDate']])
        else:
            reserves = Reserve.objects.all()
        if request.POST['choose'] == 'جدیدترین':
            reserves = reserves.order_by('-reserve_date')
        elif request.POST['choose'] == 'قدیمی ترین':
            reserves = reserves.order_by('reserve_date')
    else:
        reserves = Reserve.objects.all()
    return render(request, 'manager/reservesCheck.html', {'reserves': reserves})


@login_required
# when manager click on "accept" of a request in reserve requests page, the state of that request will change
# in this view
def accept_reserve(request, reserve_id):
    reserve = get_object_or_404(Reserve, pk=reserve_id)
    reserve.state = 'A'
    reserve.save()
    return HttpResponseRedirect(reverse('site:manager:reservesCheck'))


@login_required
# when manager click on "support request" in the menu, he can see a table include of all of his support request with
# theirs state
# can select a request to watch
# can select a request to delete
# can select a state to see all requests with that state
def requests(request):
    manager_requests = None
    if request.method == 'POST':
        manager_requests = request.user.member.manager.request_set.all()
        if request.POST['choose'] == 'W':
            manager_requests = manager_requests.filter(state='W')
        elif request.POST['choose'] == 'C':
            manager_requests = manager_requests.filter(state='C')
    else:
        manager_requests = Request.objects.all()
    return render(request, 'manager/requests.html', {'requests': manager_requests})


@login_required
def edit_n(request,neighbour_id):
    '''
    This function is for editing information of special neighbour that it's id passed in.
    Manager just can edit information like number of family member, unit number and number of account belonged to this neighbor, other information of neighbor like name and email
    are editable for neighbor's account.
    :param request:
    :param neighbour_id: for getting neighbor id for editing it.
    :return:After filling fields, if every requirements and their rule resolved, opens the page that showes every neighbor of this complex
    '''
    resident = Resident.objects.get(id=neighbour_id)
    complex = request.user.member.manager.complex
    units = Unit.objects.filter(block__complex=complex).filter(resident=None)
    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            r = form.save(commit=False)
            r.member = request.user.member
            r.save()
            return edit_neighbours(request)
    else:
        form = ResidentForm(instance=resident)

    return render(request, 'manager/editN.html', {'units': units, 'form': form, 'unit': resident.unit_id})


@login_required
def add_neighbour(request):
    '''
    Manager with this function can add all neighbour's of complex .For this, they must enter initial information of neighbours that
    include information like their real name , email, phonenumber, and also number of car, number of family member and also their individual  unit id.
    this function also generate username and password for neighbour added by manager and send it to enterd neighbor email.
    :param request: we can get manager and complex id, to get this complex's unit and specific it to this neighbour and also get form information filled by manager.
    :return: As a result of this function, if entered data doesnot have any fault, this neighbor is added to the neighbors and opened the page that shows all negibours of this complex.
    '''
    complex = request.user.member.manager.complex
    units = Unit.objects.filter(block__complex=complex).filter(resident=None)
    if request.method == 'POST':
        form1 = SignupForm2(request.POST)
        form2 = ResidentForm(request.POST)
        phoneNumber = request.POST.get('phoneNumber')
        if form1.is_valid():
            user = form1.save(commit=False)
            s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
            passlen = 8
            user.username = "".join(random.sample(s, passlen))
            password = User.objects.make_random_password()
            user.set_password(password)
            if len(phoneNumber) == 11 and phoneNumber[0:2] == '09':
                user.save()
                member = Member.objects.create(user=user, phone_number=phoneNumber)
                if form2.is_valid():
                    resident = form2.save(commit=False)
                    resident.member = member

                    member.save()
                    resident.save()
                    send_mail(
                        'ثبت نام در سامانه مدیریت مجتمع های مسکونی و آپارتمان ها ',
                        'سلام\n مدیر مجتمع {0} شما را به ثبت نام در سامانه مدیریت مجتمع دعوت کرده است. \n username:{1}\n password: {2}\n لطفا پس از ورود به سامانه نسبت به تغییر نام کاربری و رمزتان اقدام کنید.'.format(complex.name, user.username, password),
                        'fg75527@gmail.com',
                        [str(user.email)],
                        fail_silently=False,
                    )
                    return HttpResponseRedirect(reverse('site:manager:editNeighbours'))
                else:
                    user.delete()
            else:
                error = 'وارد کردن شماره تلفن الزامی است و باید 11 رقمی باشد و با 09 آغاز شود.'
                render(request, 'manager/addNeighbour.html',
                       {'form1': form1, 'form2': form2, 'units': units, 'phoneNumber': phoneNumber, 'error': error})
    else:
        return render(request, 'manager/addNeighbour.html', {'units': units})
    return render(request, 'manager/addNeighbour.html',
                  {'form1': form1, 'form2': form2, 'units': units, 'phoneNumber': phoneNumber})


@login_required
# when manager click on the "add request" in support page, a form to create request will be shown,
# after clicking on "record" a request will be created with state of "in waiting queue".
# then page will be redirected to "supporting requests" to view all the requests he created
def add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            manager_request = form.save(commit=False)
            manager_request.manager = Member.objects.filter(user=request.user)[0].manager
            manager_request.state = 'W'
            manager_request.save()
        return HttpResponseRedirect(reverse('site:manager:requests'))
    else:
        form = RequestForm()
    return render(request, 'manager/addRequest.html', {'form': form})


@login_required
def add_unit(request):
    '''
    This function is for adding Unit.
    After the manager completed complex information, is obligated to enter units and their information like area and the blocks that belong to it.
    :param request: This field need to get blocks belong to this complex and show them to manager, to choice betwen them. and also we can get
    form information and save them in database.
    :return: After filling information and press add button, if filled data doesnot have any fault, the unit and its information are added to the database
    and the page opens to show all the units of the complex.
    '''
    blocks = Block.objects.filter(complex=request.user.member.manager.complex)
    if request.method == 'POST':
        area = request.POST.get('area')
        block = request.POST.get('block')
        if area != '' and area.isdigit() and block != '':
            block = Block.objects.get(id=block)
            units = Unit.objects.filter(block=block)
            if len(units) < request.user.member.manager.complex.unit_number:
                unit = Unit.objects.create(block=block, area=int(area))
                unit.save()
                return HttpResponseRedirect(reverse('site:manager:editUnit'))
            else:
                error = 'تمام واحدهای این بلوک افزوده شده اند.'
        else:
            error = 'شماره بلوک و متراژ الزامی است.'
        return render(request, 'manager/addUnit.html', {'blocks': blocks, 'error': error})
    return render(request, 'manager/addUnit.html', {'blocks': blocks})


@login_required
def select_contact(request):
    s = Member.objects.get(user=request.user)
    ms = Message.objects.filter(Q(sender=s) | Q(receiver=s))
    return render(request, 'manager/select_contact.html', {'messages': ms})


@login_required
def message(request):
    complex = request.user.member.manager.complex
    recievers = Resident.objects.filter(unit__block__complex=complex)
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
    return render(request, 'manager/message.html', {'form': form, 'receivers': recievers})


@login_required
# when manager click on the "show" icon of a request in support page, he can see full details of that requests
def view_request(request, request_id):
    manager_request = get_object_or_404(Request, pk=request_id)
    return render(request, 'manager/viewRequest.html', {'request': manager_request})


@login_required
# when manager click on the "delete" icon of a request in support page, he can delete that requests
def delete_request(request, request_id):
    manager_request = get_object_or_404(Request, pk=request_id)
    manager_request.delete()
    return HttpResponseRedirect(reverse('site:manager:requests'))


@login_required
# when manager click on the "add bill" in menu, a form to create new bill will be shown,
# after clicking on "record" a bill will be created with date of that day.
def enter_bill(request):
    block_set = request.user.member.manager.complex.block_set.all()
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.date = datetime.now().date()
            bill.save()
    form = BillForm()
    return render(request, 'manager/enterBill.html', {'form': form, 'blocks': block_set})


@login_required
def delete_unit(request, unit_id):
    '''
    This function is for deleting special unit with id equal to eneterd 'unit_id'
    :param request:
    :param unit_id: It is id of unit, we want to delete it.
    :return: After deleting selected unit, opens the page that shows every unit of this complex.
    '''
    Unit.objects.get(id=unit_id).delete()
    return HttpResponseRedirect(reverse('site:manager:editUser'))


@login_required()
# when manager click on the "calculate charge" in calculate charge page, the charge will be calculated for all residents
# of all blocks of that complex from complex's last calculation charge date till today, like:
# for each block:
# cost of all events in this period will be summed as events_cost
# cost of all bills in this period will be summed as bills_cost
# then for each resident:
# cost of all accepted reserves in this period will be summed as reserves_cost
# an object of Receipt will be created with cost of:
# (events_cost + bills_cost)* number of members in that unit / number of members in that block + reserves_cost
# then complex's last calculation charge date will be updated to today
def calculate_receipts(request):
    complex = request.user.member.manager.complex
    for block in Block.objects.filter(complex=complex):
        size = 0
        events_cost = block.board.event_set.filter(date__gt=complex.last_calculation_date).aggregate(Sum('cost'))['cost__sum']
        bills_cost = block.bill_set.filter(date__gt=complex.last_calculation_date).aggregate(Sum('cost'))['cost__sum']
        if events_cost or bills_cost:
            for unit in block.unit_set.all():
                if unit.resident:
                    size += unit.resident.member_count
            if not events_cost:
                events_cost = 0
            if not bills_cost:
                bills_cost = 0
            for unit in block.unit_set.all():
                if unit.resident:
                    reserves_cost = unit.resident.reserve_set.filter(reserve_date__gt=complex.last_calculation_date,
                                                                     state='A').aggregate(Sum('cost'))['cost__sum']
                    c = ((events_cost + bills_cost) / size) * unit.resident.member_count
                    if reserves_cost:
                        c = c + reserves_cost
                    receipt = Receipt(start_date=complex.last_calculation_date, finish_date=datetime.today().date(),
                                      cost=c, resident=unit.resident, state='NP')
                    receipt.save()
            complex.last_calculation_date = datetime.today().date()
            complex.save()
    return HttpResponseRedirect(reverse('site:manager:viewBills'))


def edit_facility(request):
    '''
    This function is for showing all the facility of this complex.
    :param request: For getting this complex id and pass it render to show result page we need this argument.
    :return:The result of this funciton is rendering page that show every facility and their information belonged to this complex.
    '''
    complex = request.user.member.manager.complex
    facility = Facility.objects.filter(block__complex=complex)
    return render(request, 'manager/editFacility.html', {'facilities': facility})


def delete_facility(request, facility_id):
    Facility.objects.get(id=facility_id).delete()
    return HttpResponseRedirect(reverse('site:manager:editFacility'))


def add_facility(request):
    '''
    This function is for adding new facility and its information like name and its block number and its booking price.
    Only the member has access to this function.
    :param request: In addition to pass this input to the output to render html pages, we can get information like this
    complex id and it's block, to choice facility block, and enterd form data from html fields.
    :return: After adding facility and its information by manager, if entering data doesnot have any fault. This
    facillity is added to other facility of this complex and renger a page that shows every facility of this complex.
    '''
    blocks = Block.objects.filter(complex=request.user.member.manager.complex)
    if request.method == 'POST':
        name = request.POST.get('name')
        cost = request.POST.get('cost')
        block = request.POST.get('block')
        if cost != '' and cost.isdigit() and block != '' and name != '':
            block = Block.objects.get(id=block)
            facility = Facility.objects.create(type=name, cost=cost, block=block)
            facility.save()
            return HttpResponseRedirect(reverse('site:manager:editFacility'))
        else:
            error = 'وارد کردن تمام فیلدها الزامی است.'
        return render(request, 'manager/addFacility.html', {'blocks': blocks, 'error': error})
    return render(request, 'manager/addFacility.html', {'blocks': blocks})


@login_required
# when manager click on "accept" of a request in reserve requests page, the state of that request will change
# in this view
def reject_reserve(request, reserve_id):
    reserve = get_object_or_404(Reserve, pk=reserve_id)
    reserve.state = 'R'
    reserve.save()
    return HttpResponseRedirect(reverse('site:manager:reservesCheck'))


@login_required
# when manager click on the "calculate charge" in menu, he can see a table include of not paid receipts of all residents
# of all block of that complex with theirs attributes
# can select a period to see news in that period
# can select an order of seeing news
def view_bills(request):
    complex = request.user.member.manager.complex
    receipts = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            receipts = Receipt.objects.filter(state='NP', resident__unit__block__complex=complex,
                                              start_date__gte=form.cleaned_data['startDate'],
                                              start_date__lte=form.cleaned_data['finishDate'])  # TODO
        else:
            receipts = Receipt.objects.filter(state='NP', resident__unit__block__complex=complex)
        if request.POST['choose'] == 'جدیدترین':
            receipts = receipts.order_by('-start_date')
        elif request.POST['choose'] == 'قدیمی ترین':
            receipts = receipts.order_by('start_date')
    else:
        receipts = Receipt.objects.filter(state='NP', resident__unit__block__complex=complex)
    return render(request, 'manager/viewBills.html', {'receipts': receipts})
