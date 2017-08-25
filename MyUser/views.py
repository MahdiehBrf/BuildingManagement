from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from Manager.models import Manager
from MyUser.forms import LoginForm, SignupForm1
from MyUser.models import Member


def login(request):
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
    form = SignupForm1(request.POST)
    phoneNumber = request.POST.get('phoneNumber')
    context = {}
    context['phoneNumber'] = phoneNumber
    if form.is_valid():
        if len(phoneNumber) == 11 and phoneNumber[0:2] == '09':
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            member = Member.objects.create(user=user, phone_number=phoneNumber)
            member.save()
            return render(request, 'index.html', {'type': 'complexRegister'})
            ##return render(request, "manager/addNeighbour.html")
        else:
            phoneNumberError = "شماره تلفن باید 11 رقمی باشد و با 09 آغاز شود."
            context['phoneNumberError'] = phoneNumberError

    context['form'] = form
    context['type'] = "signup"
    return render(request, 'index.html', context)


def complexRegister(request):
    name = request.POST.get('name')
    address = request.POST.get('address')
    blockNum = request.POST.get('blockNum')
    context = {'name': {'value': name}, 'address': {'value': address}, 'blockNum': {'value': blockNum}}
    if name == '':
        context.get('name')['errors'] = 'نام مجتمع نباید خالی باشد.'
    elif address == '':
        context.get('address')['errors'] = 'آدرس نباید خالی باشد.'
    elif int(blockNum) < 0:
        context.get('blockNum')['errors'] = 'تعداد بلوک های مجتمع معتبر نیست.'
    else:
        pass
