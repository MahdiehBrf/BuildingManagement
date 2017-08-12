# from django.shortcuts import render
#
# # Create your views here.
from django.shortcuts import render

from MyUser.views import login,signup


def index(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'ورود':
            return login(request)
        elif request.POST.get('submit') == 'ثبت نام':
            return signup(request)
    return render(request, 'index.html')
