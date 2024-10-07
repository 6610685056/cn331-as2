from django.shortcuts import render, redirect
from .forms import RegistrationForm

# Create your views here.


def register_student(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/success.html')