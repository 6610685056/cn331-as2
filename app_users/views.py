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
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลผู้ใช้ใหม่ลงในฐานข้อมูล
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = RegisterForm()

    form = RegisterForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("home"))  # Redirect ไปยังหน้า home
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
        quota_requests = QuotaRequest.objects.filter(student=student.user)  # ข้อมูลการลงทะเบียนวิชา
        subjects = [quota_request.subject for quota_request in quota_requests]  # ดึงวิชาที่ผู้ใช้ลงทะเบียน
    except Student.DoesNotExist:
        student = None  # กรณีไม่มีข้อมูล Student
        subjects = []

    return render(request, "registration/dashboard.html", {"student": student, 'quota_requests': quota_requests, 'subjects': subjects})


@login_required
def create_student(request):
    if request.method == "POST":
        user = request.user  # ดึงข้อมูล User ที่ล็อกอินอยู่
        student_id = request.POST["student_id"]
        # สร้างข้อมูล Student เชื่อมกับ User
        student = Student.objects.create(
            user=user,
            student_id=student_id,
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            date_of_birth=request.POST["date_of_birth"],
            phone_number=request.POST["phone_number"],
            address=request.POST["address"],
            gender=request.POST["gender"],
            faculty=request.POST["faculty"],
            major=request.POST["major"],
            year_level=request.POST["year_level"],
        )
        student.save()
        return redirect(
            "student_list"
        )  # redirect ไปยังหน้ารายการนักเรียนหลังจากบันทึกข้อมูลสำเร็จ
    return render(request, "registration/create_student.html")


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
