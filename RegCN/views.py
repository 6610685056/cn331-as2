from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import QuotaRequest, Subject
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def subjects(request):
    return render(request, 'RegCN/MySubjects.html')

def subject(request, subject_id):
    return HttpResponse('subject ID= ' + str(subject_id))



@login_required
def register_subject(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, student=request.user)  # ส่ง request.user เป็น student
        if form.is_valid():
            # ตรวจสอบว่าลงทะเบียนวิชานี้ไปแล้วหรือยัง
            if QuotaRequest.objects.filter(student=request.user, subject=form.cleaned_data['subject']).exists():
                messages.error(request, "คุณได้ลงทะเบียนวิชานี้ไปแล้ว")
            else:
                form.save()  # บันทึกคำขอการลงทะเบียน
                messages.success(request, "ลงทะเบียนวิชาเรียนสำเร็จแล้ว")
                return redirect('subject_list')  # เปลี่ยนเส้นทางไปยังหน้ารายการวิชาเรียน
    else:
        form = RegistrationForm(student=request.user)  # สร้างฟอร์มสำหรับ GET request

    return render(request, 'RegCN/register_subject.html', {'form': form})  # ส่งฟอร์มไปยัง template

def subject_list(request):
    # ดึงข้อมูลวิชาที่เปิดสอน
    subjects = Subject.objects.filter(subject_is_open=True)
    return render(request, 'RegCN/subject_list.html', {'subjects': subjects})
