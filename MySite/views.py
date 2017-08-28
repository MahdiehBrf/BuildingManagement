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
    '''
    This function can be used on the front page for each user to enter the system
    or register or when they forget their password
    :param request: The request required for passing to other function and also render
    the front page of  site.
    :return: Accorfing to the user's request, it can have diffrenet outputs like rendering the
    front page of site.
    '''
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
    '''
    If user forget its password to enter the system, this function can change his password and mail
    it to the email already entered on the system. for this, user must enter his username, If his username was not in the database,
     he would not let this happen.
    :param request: For getting user request and also get username, we need this arguement.
    :return: As result of this function new password save in database and mail to user and also,
     a message saying that the password has been emailed is displayed.
    '''
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
    '''
    This function is available to all users and they can tell theri comments to the adminstrators
    and site buildrs.
    :param request:This request, define user request and we can get form information from it.
    :return:The result of this function is sending mail to site admins and reloading front page of
    site
    '''
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
    '''
    This function is to exit the system.
    :param request:For geting user request and its id.
    :return:The user is logged out and the site's first page loaded.
    '''
    auth_logout(request)
    return HttpResponseRedirect('/')
