from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from Manager.models import Manager
from MySite.models import Complex, Block, Board
from MyUser.forms import LoginForm, SignupForm1
from MyUser.models import Member


def login(request):
    '''
    This function is for entering the system, this is done for both neighbor and manager
    :param request: We can get form filled by user with this arquements and check user's request.
    :return:If the user has account and his account is active now, user can enter the system and
    this function render the home page of each section.
    '''
    form = LoginForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            member = Member.objects.get(user=user)
            try:
                Manager.objects.get(member=member)
                return HttpResponseRedirect(reverse('site:manager:account'))
            except Manager.DoesNotExist:
                return HttpResponseRedirect(reverse('site:resident:account'))
        else:
            message = 'حساب شما غیر فعال شده است.'
    else:
        message = 'نام کاربری شناخته شده نیست. لطفا ابتدا عضو شوید.'
    context = {'type': 'login', 'form': form, 'message': message}
    return render(request, 'index.html', context)


def signup(request):
    '''
    This function is only for manager to enter their infomation and register themself in site.
    :param request: Contains user request information and form data that user entered
    :return: As result of this function, if entering data hasnot have any fault. open other form
    for gettin complex information and register it.
    of manager section. otherwise shows errors of entering data in front page of site.
    '''
    form = SignupForm1(request.POST)
    phoneNumber = request.POST.get('phoneNumber')
    accountNumber = request.POST.get('accountNumber')
    context = {}
    context['phoneNumber'] = phoneNumber
    context['accountNumber'] = accountNumber
    if form.is_valid():
        if len(phoneNumber) == 11 and phoneNumber[0:2] == '09':
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            member = Member.objects.create(user=user, phone_number=phoneNumber)
            member.save()
            manager = Manager.objects.create(member=member, bank_account_num=accountNumber)
            manager.save()
            return render(request, 'index.html', {'type': 'complexRegister'})
        else:
            phoneNumberError = "شماره تلفن باید 11 رقمی باشد و با 09 آغاز شود."
            context['phoneNumberError'] = phoneNumberError

    context['form'] = form
    context['type'] = "signup"
    return render(request, 'index.html', context)


def complexRegister(request):
    '''
    This function is available after the manager entered his information, and gives data such as
    complex name, address, number of block of complex and number of units inside blocks.
    :param request:We can get form information from this request.POST. and also pass it to output
    to render next page.
    :return:Result of this function is registering and saveing complex information in database and assign it
    to manager. and if entering information for complex doesnt have any error after pressing save buttom,
    the main page of manager seciton opened.
    '''
    name = request.POST.get('name')
    address = request.POST.get('address')
    blockNum = request.POST.get('blockNumber')
    unit_per_block = request.POST.get('unit_per_block')
    context = {'name': {'value': name}, 'address': {'value': address}, 'blockNum': {'value': blockNum},
               'unit_per_block': {'value': unit_per_block},
               'type': 'complexRegister'}
    if name == '':
        context.get('name')['errors'] = 'نام مجتمع نباید خالی باشد.'
    elif address == '':
        context.get('address')['errors'] = 'آدرس نباید خالی باشد.'
    elif blockNum.isdigit() and int(blockNum) < 1:
        context.get('blockNum')['errors'] = 'تعداد بلوک های مجتمع معتبر نیست.'
    elif unit_per_block.isdigit() and int(unit_per_block) < 1:
        context.get('unit_per_block')['errors'] = 'تعداد واحدهای هر بلوک معتبر نیست.'
    else:
        manager = request.user.member.manager
        complex = Complex.objects.create(manager=manager, name=name, address=address, unit_number=int(unit_per_block))
        complex.save()
        for i in range(int(blockNum)):
            block = Block.objects.create(complex=complex)
            block.save()
            board = Board.objects.create(block=block)
            board.save()
        return HttpResponseRedirect(reverse('site:manager:account'))
    return render(request, 'index.html', context)
