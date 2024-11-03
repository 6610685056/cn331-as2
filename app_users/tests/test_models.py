from django.test import TestCase
from django.contrib.auth.models import User
from app_users.models import Student


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.student = Student.objects.create(
            user=self.user,
            student_id="123456",
            first_name="John",
            last_name="Doe",
            date_of_birth="2000-01-01",
            email="john@example.com",
            phone_number="1234567890",
            address="123 Main St",
            gender="M",
            faculty="Engineering",
            major="Computer Science",
            year_level=2,
        )

    def test_student_str(self):
        # ทดสอบการแสดงผลของ __str__ method
        self.assertEqual(str(self.student), "John Doe (123456)")
