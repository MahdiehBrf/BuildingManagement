import django
from django.contrib.auth.models import User
from django import forms

from MyUser.models import Member
from Resident.models import Resident

class Resident_UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email']

class ResidentForm(django.forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['member_count','car_count','unit']