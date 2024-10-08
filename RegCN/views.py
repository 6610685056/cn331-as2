from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from .models import QuotaRequest, Subject
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_users.models import Student

def subjects(request):
    return render(request, "RegCN/MySubjects.html")

def subject(request, subject_id):
    return HttpResponse("subject ID= " + str(subject_id))

@login_required
def register_subject(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, student=request.user)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            if QuotaRequest.objects.filter(student=request.user, subject=subject).exists():
                messages.error(request, "คุณได้ลงทะเบียนวิชานี้ไปแล้ว")
            else:
                form.save()  # บันทึกคำขอการลงทะเบียน
                messages.success(request, "ลงทะเบียนวิชาเรียนสำเร็จแล้ว")
                return redirect("dashboard")
    else:
        form = RegistrationForm(student=request.user)

    return render(request, "RegCN/register_subject.html", {"form": form})

@login_required
def subject_list(request):
    subjects = Subject.objects.filter(subject_is_open=True)
    return render(request, "RegCN/subject_list.html", {"subjects": subjects})

@login_required
def drop_subject(request, subject_id):
    student = Student.objects.get(user=request.user)  # รับข้อมูลนักเรียนที่ล็อกอิน
    quota_request = get_object_or_404(QuotaRequest, student=student.user, subject__subject_id=subject_id)
    
    if request.method == 'POST':
        quota_request.delete()  # ลบการลงทะเบียนวิชานี้ออกจากฐานข้อมูล
        messages.success(request, "ถอนวิชาสำเร็จแล้ว")
        return redirect('dashboard')  # เปลี่ยนเส้นทางไปยังหน้า Dashboard

    return render(request, 'RegCN/confirm_drop.html', {'subject': quota_request.subject})
