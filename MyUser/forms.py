
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from MyUser.models import Member


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class SignupForm1(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',"password1", "password2")


class SignupForm2(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'