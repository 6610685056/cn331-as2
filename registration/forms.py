from django import forms
from .models import Student, Course, Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['student', 'course']