from django import forms
from .models import Tasks


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    class Meta:
        model = User
        fields = ['username', 'email']


        
class Task_form(forms.ModelForm):
    class Meta:
        model = Tasks
        # excepts = ['user']
        exclude = ['user']