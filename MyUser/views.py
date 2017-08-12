from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render

# Create your views here.
from MyUser.forms import LoginForm


def login(request):
    form = LoginForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return render(request, "addNeighbour.html")
        else:
            message = 'حساب شما غیر فعال شده است.'
    else:
        message = 'نام کاربری شناخته شده نیست. لطفا ابتدا عضو شوید.'
    context = {'type': 'login', 'form': form, 'message': message}
    return render(request, 'index.html', context)


def signup(reqest):
    pass
