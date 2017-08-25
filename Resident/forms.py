import django
from django.contrib.auth.models import User
from django import forms

from MyUser.models import Member, Message
from Resident.models import Resident, Reserve


class Resident_UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email']


class ResidentForm(django.forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['member_count', 'car_count', 'unit']


class ReserveForm(django.forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['facility']

class DateForm(django.forms.Form):
    use_startDate_0 = forms.DateField()
    use_startDate_1 = forms.TimeField()
    use_finishDate_0 = forms.DateField()
    use_finishDate_1 = forms.TimeField()

class MessageForm(django.forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'theme_type']