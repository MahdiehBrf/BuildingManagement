import django
from django.contrib.auth.models import User
from django.forms import TextInput

from Manager.models import Manager


class ManagerForm(django.forms.ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
