from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Student


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User  # ระบุโมเดลที่ใช้กับฟอร์ม
        fields = ['username', 'email', 'password1','password2']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'date_of_birth', 
                  'phone_number', 'address', 'gender','faculty', 'major', 'year_level']

