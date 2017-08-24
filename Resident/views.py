from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from MySite.forms import DisplayForm
from MySite.models import News, Event


def account(request):
    return render(request, 'resident/account.html')


@login_required
def view_board(request):
    resident = request.user.member.resident
    events = None
    news_set = None
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            news_set = resident.unit.block.board.news_set.filter(board__block=resident.unit.block, date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
            events = resident.unit.block.board.event_set.filter(board__block=resident.unit.block, date__gte=form.cleaned_data['startDate'], date__lte=form.cleaned_data['finishDate'])
        else:
            news_set = resident.unit.block.board.news_set.all()
            events = resident.unit.block.board.event_set.all()
        if request.POST['choose'] == 'جدیدترین':
            news_set = news_set.order_by('-date')
            events = events.order_by('-date')
    else:
        news_set = resident.unit.block.board.news_set.all()
        events = resident.unit.block.board.event_set.all()
    return render(request, 'resident/board.html', {'events': events, 'newsSet': news_set})


def edit_profile(request):
    return render(request, 'resident/edit_profile.html')


def paying_reports(request):
    return render(request, 'resident/payingReports_user.html')


def reserve(request):
    return render(request, 'resident/reserve.html')


def message(request):
    return render(request, 'resident/message.html')


def select_contact(request):
    return render(request, 'resident/select_contact.html')


def view_bills(request):
    return render(request, 'resident/bills.html')


def view_reserves(request):
    return render(request, 'resident/myReserves.html')


def view_bill(request):
    return render(request, 'resident/viewBill.html')