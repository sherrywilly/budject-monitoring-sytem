from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from userapp.models import Expense
from django import forms

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name','desc','amount','department']
        
class ProfileUpdate(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password']
