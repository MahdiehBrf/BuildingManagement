import django
from django.contrib.auth.models import User
from django.forms import TextInput

from Manager.models import Manager, Request


class ManagerForm(django.forms.ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'


class RequestForm(django.forms.ModelForm):
    class Meta:
        model = Request
        exclude = ['manager', 'state']
