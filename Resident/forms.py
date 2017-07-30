import django
from django.contrib.auth.models import User
from django import forms

from MyUser.models import Member
from Resident.models import Resident


class ResidentForm(django.forms.ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'