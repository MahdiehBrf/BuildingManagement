from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from MySite.forms import EventForm, NewsForm, DisplayForm
from MySite.models import Event, News


def account(request):
    return render(request, 'account.html')


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
    return render(request, 'add_to_board.html', {'form': form})


def view_board(request):
    events = None
    news_set = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            news_set = News.objects.filter(date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
            events = Event.objects.filter(date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
        else:
            news_set = News.objects.all()
            events = Event.objects.all()
        if request.POST['choose'] == 'جدیدترین':
            news_set = news_set.order_by('-date')
            events = events.order_by('-date')
    else:
        news_set = News.objects.all()
        events = Event.objects.all()
    return render(request, 'board.html', {'events': events, 'newsSet': news_set})


def edit_profile(request):
    return render(request, 'edit_profile.html')


def edit_complex_information(request):
    return render(request, 'edit_complex_information.html')


def edit_neighbours(request):
    return render(request, 'editNeighbours.html')


def edit_unit(request):
    return render(request, 'editUnit.html')


def paying_reports(request):
    return render(request, 'payingReports.html')


def reserves_check(request):
    return render(request, 'reservesCheck.html')


def requests(request):
    return render(request, 'requests.html')


def add_neighbour(request):
    return render(request, 'addNeighbour.html')


def add_request(request):
    return render(request, 'addRequest.html')


def add_unit(request):
    return render(request, 'addUnit.html')


def edit_n(request):
    return render(request, 'editN.html')


def message(request):
    return render(request, 'message.html')


def select_contact(request):
    return render(request, 'select_contact.html')


def view_request(request):
    return render(request, 'viewRequest.html')
