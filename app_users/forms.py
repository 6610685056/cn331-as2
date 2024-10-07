from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User  # ระบุโมเดลที่ใช้กับฟอร์ม
        fields = ['username', 'email', 'password1','password2']

