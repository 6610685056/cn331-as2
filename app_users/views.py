# import method คำสั่งต่างๆ

from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm, StudentForm, Student
from RegCN.models import QuotaRequest

# Create your views here.


def register(request: HttpRequest):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลผู้ใช้ใหม่ลงในฐานข้อมูล
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return HttpResponseRedirect(reverse("home_page:home"))

    context = {"form": form}
    return render(request, "registration/register.html", context)


def student_list(request):
    students = Student.objects.all()  # ดึงข้อมูลนักเรียนทั้งหมด
    return render(request, "registration/student_list.html", {"students": students})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect(reverse("home"))
        else:
            return render(
                request, "login.html", {"error": "Invalid username or password"}
            )
    else:
        return render(request, "login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


@login_required
def dashboard(request: HttpRequest):
    quota_requests = None
    try:
        student = Student.objects.get(user=request.user)
        quota_requests = QuotaRequest.objects.filter(
            student=student.user
        )  # ข้อมูลการลงทะเบียนวิชา
        subjects = [
            quota_request.subject for quota_request in quota_requests
        ]  # ดึงวิชาที่ผู้ใช้ลงทะเบียน
    except Student.DoesNotExist:
        student = None  # กรณีไม่มีข้อมูล Student
        subjects = []

    return render(
        request,
        "registration/dashboard.html",
        {"student": student, "quota_requests": quota_requests, "subjects": subjects},
    )


@login_required
def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)  # ยังไม่บันทึกลงฐานข้อมูล
            student.user = request.user  # เชื่อมกับผู้ใช้ที่ล็อกอิน
            student.save()  # บันทึกลงฐานข้อมูล
            return redirect("student_list")  # เปลี่ยนไปยังหน้ารายการนักเรียน
    else:
        form = StudentForm()
    return render(request, "registration/create_student.html", {"form": form})
