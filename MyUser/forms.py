import django
from django import forms

from MyUser.models import Member


class LoginForm(django.forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'password']

class MessageForm(django.forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'