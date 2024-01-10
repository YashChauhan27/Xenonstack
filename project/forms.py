from django import forms
from .models import User

class User(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email']