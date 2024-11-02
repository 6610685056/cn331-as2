from django.test import TestCase
from django.contrib.auth.models import User
from RegCN.models import Subject, QuotaRequest
import datetime

class SubjectModelTest(TestCase):
    def setUp(self):
        # สร้าง Subject สำหรับการทดสอบ
        self.subject = Subject.objects.create(
            title="Mathematics",
            subject_id="MATH01",
            subject_term="1",
            subject_year=2024,
            avilable_seat=30,
            subject_is_open=True
        )

    def test_subject_creation(self):
        # ทดสอบการสร้าง Subject
        self.assertEqual(self.subject.title, "Mathematics")
        self.assertEqual(self.subject.subject_id, "MATH01")
        self.assertEqual(self.subject.subject_term, "1")
        self.assertEqual(self.subject.subject_year, 2024)
        self.assertEqual(self.subject.avilable_seat, 30)
        self.assertTrue(self.subject.subject_is_open)

    def test_subject_str_method(self):
        # ทดสอบ __str__ method
        self.assertEqual(
            str(self.subject),
            "MATH01 - Mathematics (2024 Term 1)"
        )

class QuotaRequestModelTest(TestCase):
    def setUp(self):
        # สร้าง User และ Subject สำหรับการทดสอบ QuotaRequest
        self.user = User.objects.create_user(username="student1", password="testpass")
        self.subject = Subject.objects.create(
            title="Science",
            subject_id="SCI01",
            subject_term="2",
            subject_year=2024,
            avilable_seat=20,
            subject_is_open=True
        )
        self.quota_request = QuotaRequest.objects.create(
            student=self.user,
            subject=self.subject,
            approved=False,
            rejected=False
        )

    def test_quota_request_creation(self):
        # ทดสอบการสร้าง QuotaRequest
        self.assertEqual(self.quota_request.student.username, "student1")
        self.assertEqual(self.quota_request.subject.title, "Science")
        self.assertFalse(self.quota_request.approved)
        self.assertFalse(self.quota_request.rejected)
        self.assertIsNotNone(self.quota_request.request_date)

    def test_quota_request_str_method(self):
        # ทดสอบ __str__ method
        self.assertEqual(
            str(self.quota_request),
            "student1 - Science"
        )

