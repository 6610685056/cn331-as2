from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_users.models import Student
from app_users.forms import RegisterForm, StudentForm
from django.contrib.auth import get_user_model
from django.test import override_settings
from RegCN.models import Subject, QuotaRequest


class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_view_post_valid(self):
        data = {
            "username": "newuser",
            "password1": "validpassword123",
            "password2": "validpassword123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)  # ตรวจสอบว่า redirect เมื่อสำเร็จ
        self.assertRedirects(
            response, reverse("home_page:home")
        )  # ปรับ URL ให้ตรงกับหน้า redirect หลังจาก register สำเร็จ
        # ตรวจสอบว่า user ถูกสร้างขึ้นในฐานข้อมูล
        self.assertTrue(User.objects.filter(username="newuser").exists())

    @override_settings(LANGUAGE_CODE="en")
    def test_register_view_post_invalid(self):
        data = {
            "username": "",  # ไม่ใส่ username เพื่อให้ form ไม่ valid
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "This field is required.")

    @override_settings(LANGUAGE_CODE="en")
    def test_register_view_post_missing_username(self):
        data = {
            "username": "",  # ไม่ใส่ username
            "password1": "password123",
            "password2": "password123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "This field is required.")

    @override_settings(LANGUAGE_CODE="en")
    def test_register_view_post_existing_username(self):
        # สร้าง user ก่อนเพื่อให้ username มีอยู่ในระบบแล้ว
        User.objects.create_user(username="existinguser", password="12345")
        data = {
            "username": "existinguser",
            "password1": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "A user with that username already exists.")

    @override_settings(LANGUAGE_CODE="en")
    def test_register_view_post_password1_only(self):
        data = {
            "username": "testuser",
            "password1": "password123",
            "password2": "",  # ไม่กรอก password2
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "This field is required.")

    @override_settings(LANGUAGE_CODE="en")
    def test_register_view_post_invalid_password_mismatch(self):
        data = {
            "username": "testuser",
            "password1": "password123",
            "password2": "password456",  # ใส่ password ไม่ตรงกัน
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "The two password fields didn’t match.")

    @override_settings(LANGUAGE_CODE="en")
    def test_register_view_post_short_password(self):
        data = {
            "username": "newuser",
            "password1": "short",
            "password2": "short",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(
            response,
            "This password is too short. It must contain at least 8 characters.",
        )

    def test_register_view_post_invalid_missing_fields(self):
        # กรณีส่ง POST โดยไม่กรอกข้อมูล
        response = self.client.post(reverse("register"), {})
        self.assertEqual(
            response.status_code, 200
        )  # ฟอร์มควรจะกลับมาที่หน้าเดิมพร้อม error message
        self.assertContains(
            response, "This field is required."
        )  # ตรวจสอบว่ามี error message

    def test_login_view(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "12345"}
        )
        self.assertRedirects(response, reverse("home_page:home"))

    def test_logout_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_logout_view_get(self):
        # ทดสอบกรณีเรียก logout ด้วย GET ควรจะคืนค่า 405
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_dashboard_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/dashboard.html")

    def test_dashboard_view_without_student(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/dashboard.html")
        self.assertContains(response, "ไม่พบข้อมูลนักเรียนในระบบ")

    def test_dashboard_view_with_student_but_no_quota_requests(self):
        # สร้าง student โดยไม่มีการลงทะเบียนวิชา
        user = User.objects.create_user(username="studentuser", password="password123")
        Student.objects.create(
            user=user,
            student_id="123456",
            date_of_birth="2000-01-01",  # ระบุ date_of_birth เพื่อไม่ให้เกิด IntegrityError
        )

        self.client.login(username="studentuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/dashboard.html")
        self.assertContains(response, "ยังไม่ได้ลงทะเบียนวิชาใดๆ")

    def test_dashboard_view_with_student_and_quota_requests(self):
        # สร้าง student พร้อมกับข้อมูล date_of_birth
        user = User.objects.create_user(username="studentuser", password="password123")
        student = Student.objects.create(
            user=user,
            student_id="123456",
            date_of_birth="2000-01-01",  # เพิ่มข้อมูล date_of_birth
        )
        subject = Subject.objects.create(
            title="Mathematics",
            subject_id="MATH01",
            subject_term="1",
            subject_year=2023,
            avilable_seat=30,
            subject_is_open=True,
        )
        QuotaRequest.objects.create(student=user, subject=subject)

        self.client.login(username="studentuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/dashboard.html")
        self.assertContains(response, "Mathematics")

    def test_dashboard_view_non_student_user(self):
        # สร้างผู้ใช้ทั่วไปที่ไม่ใช่ student
        user = User.objects.create_user(
            username="nonstudentuser", password="password123"
        )

        self.client.login(username="nonstudentuser", password="password123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/dashboard.html")
        self.assertContains(response, "ไม่พบข้อมูลนักเรียนในระบบ")

    def test_create_student_view_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("create_student"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/create_student.html")

    def test_create_student_view_post(self):
        self.client.login(username="testuser", password="password123")
        data = {
            "student_id": "123456",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            "gender": "M",
            "faculty": "Engineering",
            "major": "Computer Science",
            "year_level": 2,
        }
        response = self.client.post(reverse("create_student"), data)
        self.assertRedirects(response, reverse("student_list"))
        self.assertTrue(Student.objects.filter(student_id="123456").exists())

    def test_create_student_post_invalid(self):
        # ทดสอบการสร้าง student แบบ POST ข้อมูลไม่ครบ
        data = {
            "student_id": "12345",
            # ข้อมูลไม่ครบ เช่น ไม่มี first_name
        }
        response = self.client.post(reverse("create_student"), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/create_student.html")
        self.assertContains(response, "This field is required.")

    def test_login_success_with_next_parameter(self):
        response = self.client.post(
            reverse("login") + "?next=" + reverse("dashboard"),
            {"username": "testuser", "password": "12345"},
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_success_without_next_parameter(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "12345"}
        )
        self.assertRedirects(response, reverse("home_page:home"))

    def test_login_invalid(self):
        data = {"username": "wronguser", "password": "wrongpassword"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 200)
        # เปลี่ยนข้อความที่ตรวจสอบให้ตรงกับข้อความใน HTML
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")
    
