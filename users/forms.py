from django import forms
from users.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("avatar", "first_name", "last_name", "email", "password")
