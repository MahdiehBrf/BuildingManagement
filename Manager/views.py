from django.shortcuts import render

# Create your views here.
from django.utils.datetime_safe import datetime

from MySite.forms import EventForm, NewsForm
from MySite.models import Event, News


def account(request):
    return render(request, 'account.html')


def add_to_board(request):
    form = EventForm()
    return render(request, 'add_to_board.html')


def view_board(request):
    if request.method == 'POST':
        if request.POST['choose'] == 'event':
            form = EventForm(request.POST)
            if form.is_valid():
                event = Event(date_time=datetime.now(), description=form.cleaned_data['description'], cost=form.cleaned_data['cost'])
        else:
            form = NewsForm(request)
            if form.is_valid():
                news = News(date_time=datetime.now(), description=form.cleaned_data['description'],
                              title=form.cleaned_data['title'])
    else:
        pass
    return render(request, 'board.html')