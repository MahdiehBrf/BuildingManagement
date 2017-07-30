import django
from django.contrib.auth.models import User
from django import forms

from MyUser.models import Member


class LoginForm(django.forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class MessageForm(django.forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'