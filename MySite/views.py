# from django.shortcuts import render
#
# # Create your views here.
from django.core.mail import send_mail
from django.shortcuts import render

from MyUser.views import login,signup


def index(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'ورود':
            return login(request)
        elif request.POST.get('submit') == 'ثبت نام':
            return signup(request)
    return render(request, 'index.html')


def send_feedback(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lnaem = request.POST.get('last_name')
        email = request.POST.get('email')
        content = request.POST.get('content')

        send_mail(
            'Feedback Message From Site Visitor',
            content + "\n From {0}  {1}".format(fname,lnaem),
            'fg75527@gmail.com',
            [str(email)],
            fail_silently=False,
        )


    return render(request, 'index.html')
