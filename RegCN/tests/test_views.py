from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from RegCN.models import Subject, QuotaRequest
from app_users.models import Student


class SubjectsViewTest(TestCase):
    def test_subjects_view_status_code(self):
        response = self.client.get(reverse("subjects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home_page/home.html")


class SubjectViewTest(TestCase):
    def test_subject_view_status_code(self):
        response = self.client.get(reverse("subject", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "subject ID= 1")


class RegisterSubjectViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และล็อกอิน
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.student = Student.objects.create(
            user=self.user, date_of_birth="2000-01-01"
        )
        self.client.login(username="testuser", password="12345")
        # สร้าง Subject
        self.subject = Subject.objects.create(
            title="Mathematics", subject_id="MATH01", subject_is_open=True
        )

    def test_register_subject_get(self):
        # ตรวจสอบการเข้าถึงหน้า register_subject
        response = self.client.get(reverse("register_subject"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RegCN/register_subject.html")

    def test_register_subject_post_success(self):
        # ตรวจสอบการลงทะเบียนวิชาสำเร็จ
        response = self.client.post(
            reverse("register_subject"), {"subject": self.subject.subject_id}
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))
        self.assertEqual(messages[0].level_tag, "success")
        self.assertEqual(str(messages[0]), "ลงทะเบียนวิชาเรียนสำเร็จแล้ว")

    def test_register_subject_post_duplicate(self):
        # ตรวจสอบการลงทะเบียนซ้ำ
        QuotaRequest.objects.create(student=self.user, subject=self.subject)
        response = self.client.post(
            reverse("register_subject"), {"subject": self.subject.subject_id}
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0].level_tag, "error")
        self.assertEqual(str(messages[0]), "คุณได้ลงทะเบียนวิชานี้ไปแล้ว")


class SubjectListViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และล็อกอิน
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.student = Student.objects.create(
            user=self.user, date_of_birth="2000-01-01"
        )
        self.client.login(username="testuser", password="12345")
        # สร้าง Subject
        self.subject = Subject.objects.create(
            title="Science", subject_id="SCI01", subject_is_open=True
        )

    def test_subject_list_view(self):
        response = self.client.get(reverse("subject_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RegCN/subject_list.html")
        self.assertIn(self.subject, response.context["subjects"])


class DropSubjectViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้, นักเรียน, และล็อกอิน
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.student = Student.objects.create(
            user=self.user, date_of_birth="2000-01-01"
        )
        self.client.login(username="testuser", password="12345")
        # สร้าง Subject และ QuotaRequest
        self.subject = Subject.objects.create(
            title="History", subject_id="HIST01", subject_is_open=True
        )
        self.quota_request = QuotaRequest.objects.create(
            student=self.user, subject=self.subject
        )

    def test_drop_subject_get(self):
        # ตรวจสอบการเข้าถึงหน้า drop_subject
        response = self.client.get(
            reverse("drop_subject", args=[self.subject.subject_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RegCN/confirm_drop.html")

    def test_drop_subject_post(self):
        # ตรวจสอบการถอนวิชาสำเร็จ
        response = self.client.post(
            reverse("drop_subject", args=[self.subject.subject_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].level_tag, "success")
        self.assertEqual(str(messages[0]), "ถอนวิชาสำเร็จแล้ว")
        self.assertFalse(
            QuotaRequest.objects.filter(
                student=self.user, subject=self.subject
            ).exists()
        )
