from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

# Create your models here.

# ตัวเลือกภาคการศึกษา
term_choice = [
    ("1", "First Term"),
    ("2", "Second Term"),
]

# ปีที่สามารถเลือกได้
YEAR_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year + 1)]


# โมเดลสำหรับวิชา (Subject)
class Subject(models.Model):
    title = models.CharField(max_length=60)
    subject_id = models.CharField(max_length=6, primary_key=True)
    subject_term = models.CharField(max_length=6, choices=term_choice, default="1")
    subject_year = models.IntegerField(
        choices=YEAR_CHOICES, default=datetime.datetime.now().year
    )
    avilable_seat = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    subject_is_open = models.BooleanField()

    def __str__(self):
        return f"{self.subject_id} - {self.title} ({self.subject_year} Term {self.subject_term})"


class QuotaRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # นักเรียนที่ขอโควต้า
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # วิชาที่ต้องการขอโควต้า
    request_date = models.DateTimeField(auto_now_add=True)  # วันที่ขอ
    approved = models.BooleanField(default=False)  # อนุมัติหรือไม่
    rejected = models.BooleanField(default=False)  # ปฏิเสธหรือไม่

    def __str__(self):
        return f"{self.student.username} - {self.subject.title}"
