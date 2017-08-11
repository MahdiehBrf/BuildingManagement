from django import forms
import django

from MySite.models import Complex, News, Event


class ComplexForm(django.forms.ModelForm):
    class Meta:
        model = Complex
        fields = '__all__'


# class ReserveForm(django.forms.ModelForm):
#     class Meta:
#         model = Reserve
#         exclude = ['reserve_date']


class NewsForm(django.forms.ModelForm):
    class Meta:
        model = News
        fields = ['board', 'date_time']


class EventForm(django.forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['board', 'date_time']


# class ReceiptForm(django.forms.ModelForm):
#     class Meta:
#         model = Receipt
#         fields = '__all__'
