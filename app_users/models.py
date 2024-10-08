from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    student_id = models.CharField(max_length=10, unique=True)  # รหัสนักเรียน
    first_name = models.CharField(max_length=100)  # ชื่อ
    last_name = models.CharField(max_length=100)  # นามสกุล
    date_of_birth = models.DateField()  # วันเกิด
    email = models.EmailField(unique=True)  # อีเมล
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # เบอร์โทรศัพท์
    address = models.TextField(blank=True, null=True)  # ที่อยู่
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="O")  # เพศ
    faculty = models.CharField(max_length=100, blank=True, null=True)  # คณะวิชา
    major = models.CharField(max_length=100, blank=True, null=True)  # สาขาวิชา
    year_level = models.IntegerField(default=1)  # ปีการศึกษา
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
