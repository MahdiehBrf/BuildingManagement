# from django.shortcuts import render
#
# # Create your views here.
from django.contrib.auth import logout as auth_logout
from django.core.mail import mail_admins
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
    return render(request, 'index.html')




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
