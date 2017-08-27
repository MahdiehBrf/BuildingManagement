# from django.shortcuts import render
#
# # Create your views here.
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import mail_admins, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from MyUser.views import login, signup, complexRegister


def index(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'ورود':
            return login(request)
        elif request.POST.get('submit') == 'ثبت نام':
            return signup(request)
        elif request.POST.get('submit') == 'ثبت نام مجتمع':
            return complexRegister(request)
        else:
            return forget_password(request)
    return render(request, 'index.html')

def forget_password(request):
    username = request.POST['username']
    if username != '':
        try:
            user = User.objects.get(username=username)
            if user:
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                send_mail(
                    'بازیابی رمز عبور ',
                    'کاربر محترم {0} رمز شما به رمز زیر تغییر نمود. لطفا به تغییر رمز خود اقدام کنید.\n password: {1}'.format(user.first_name + '  ' +user.last_name, password),
                    'fg75527@gmail.com',
                    [str(user.email)],
                    fail_silently=False,
                )
                message = 'رمز عبور جدید به ایمیلتان فرستاده شد.'
                context = {'type': 'login', 'message': message}
                return render(request, 'index.html', context)
        except User.DoesNotExist:
                message = 'نام کاربری شناخته شده نیست.'
    else:
        message = 'جهت بازیابی رمز عبور، نام کاربری تان را وارد کنید.'
    context = {'type': 'forget_password',  'message': message}
    return render(request, 'index.html', context)


def send_feedback(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        content = request.POST.get('text')
        mail_admins(
            'Feedback Message From Site Visitor',
            "Message Content : "+str(content) + "\n From {0} and {1}\n and Email {2}".format(fname,lname,email),
            'fg75527@gmail.com',
        )
    return HttpResponseRedirect('/')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
