#import method คำสั่งต่างๆ

from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm

# Create your views here.

def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลผู้ใช้ใหม่ลงในฐานข้อมูล
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return HttpResponseRedirect(reverse("home"))
        else:
            form = RegisterForm()


    form = RegisterForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))  # Redirect ไปยังหน้า home
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    


@login_required
def dashboard(request: HttpRequest):
    return render(request, "registration/dashboard.html")