from django import forms
import django

from MySite.models import Reserve, Complex, News, Event, Receipt


class ComplexForm(django.forms.ModelForm):
    class Meta:
        model = Complex
        fields = '__all__'


class ReserveForm(django.forms.ModelForm):
    class Meta:
        model = Reserve
        exclude = ['reserve_date']


class NewsForm(django.forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'


class EventForm(django.forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class ReceiptForm(django.forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
