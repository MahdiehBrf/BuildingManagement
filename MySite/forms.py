import django
from django import forms

from MySite.models import Complex, News, Event


class ComplexForm(django.forms.ModelForm):
    class Meta:
        model = Complex
        fields = ['name', 'address']


# class ReserveForm(django.forms.ModelForm):
#     class Meta:
#         model = Reserve
#         exclude = ['reserve_date']


class NewsForm(django.forms.ModelForm):
    class Meta:
        model = News
        exclude = ['date']


class EventForm(django.forms.ModelForm):

    class Meta:
        model = Event
        exclude = ['date']


# class ReceiptForm(django.forms.ModelForm):
#     class Meta:
#         model = Receipt
#         fields = '__all__'


class DisplayForm(django.forms.Form):
    startDate = django.forms.DateField()
    finishDate = django.forms.DateField()
