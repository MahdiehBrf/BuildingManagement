
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from MyUser.models import Member


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class SignupForm1(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=50, required=True)
    lastname = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username','firstname','lastname','email',"password1", "password2")


class SignupForm2(forms.ModelForm):
    pass

class MessageForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'