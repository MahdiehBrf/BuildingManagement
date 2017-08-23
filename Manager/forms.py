import django
from django.forms import TextInput

from Manager.models import Manager, Request
from MyUser.models import Message


class ManagerForm(django.forms.ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'


class RequestForm(django.forms.ModelForm):
    class Meta:
        model = Request
        exclude = ['manager', 'state']


class MessageForm(django.forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['sender', 'theme_type']
