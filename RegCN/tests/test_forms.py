from django.test import TestCase
from django.contrib.auth.models import User
from RegCN.forms import RegistrationForm
from RegCN.models import Subject, QuotaRequest


class RegistrationFormTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และ subject ที่จะใช้ในการทดสอบ
        self.student_user = User.objects.create_user(
            username="student1", password="testpass"
        )
        self.open_subject = Subject.objects.create(
            title="Open Subject", subject_id="MATH01", subject_is_open=True
        )
        self.closed_subject = Subject.objects.create(
            title="Closed Subject", subject_id="HIST01", subject_is_open=False
        )

    def test_form_init_filters_subjects(self):
        # ตรวจสอบว่า subject ที่ปิดไม่ให้ลงทะเบียนจะไม่อยู่ในฟอร์ม
        form = RegistrationForm(
            {"subject": self.open_subject.subject_id}, student=self.student_user
        )
        self.assertIn(self.open_subject, form.fields["subject"].queryset)
        self.assertNotIn(self.closed_subject, form.fields["subject"].queryset)

    def test_form_is_valid(self):
        # ตรวจสอบว่า form ถูกต้องเมื่อมีการส่ง subject ที่เปิดให้ลงทะเบียน
        open_subject = Subject.objects.create(
            title="Open Subject", subject_id="MATH02", subject_is_open=True
        )
        form = RegistrationForm(
            data={"subject": open_subject.subject_id}, student=self.student_user
        )
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_closed_subject(self):
        # ตรวจสอบว่า form ไม่ถูกต้องเมื่อส่ง subject ที่ปิดไม่ให้ลงทะเบียน
        form = RegistrationForm(
            data={"subject": self.closed_subject.subject_id}, student=self.student_user
        )
        self.assertFalse(form.is_valid())

    def test_form_save_with_student_and_commit_true(self):
        # ทดสอบการ save เมื่อมี student และ commit=True
        form = RegistrationForm(
            data={"subject": self.open_subject.subject_id}, student=self.student_user
        )
        self.assertTrue(form.is_valid())
        quota_request = form.save(commit=True)
        self.assertEqual(quota_request.student, self.student_user)
        self.assertEqual(quota_request.subject, self.open_subject)

    def test_form_save_with_student_and_commit_false(self):
        # ทดสอบการ save เมื่อมี student และ commit=False
        form = RegistrationForm(
            data={"subject": self.open_subject.subject_id}, student=self.student_user
        )

        # ตรวจสอบว่า form เป็น valid และพิมพ์ errors หากมี
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

        # บันทึกฟอร์มโดยใช้ commit=False
        quota_request = form.save(commit=False)
        self.assertEqual(quota_request.student, self.student_user)
        self.assertEqual(quota_request.subject, self.open_subject)
        self.assertFalse(
            QuotaRequest.objects.filter(
                student=self.student_user, subject=self.open_subject
            ).exists()
        )

    def test_form_save_without_student(self):
        # ทดสอบการ save เมื่อไม่มี student
        form = RegistrationForm({"subject": self.open_subject.subject_id})
        self.assertTrue(form.is_valid())
        quota_request = form.save(commit=True)
        self.assertIsNone(quota_request.student)
        self.assertEqual(quota_request.subject, self.open_subject)

    def test_form_save_without_student_and_commit_false(self):
        open_subject = Subject.objects.create(
            title="Open Subject", subject_id="MATH03", subject_is_open=True
        )
        # ทดสอบการ save เมื่อไม่มี student และ commit=False
        form = RegistrationForm(data={"subject": open_subject.subject_id})
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
        quota_request = form.save(commit=False)

        self.assertIsNone(quota_request.student)  # ตรวจสอบว่า student เป็น None

        self.assertEqual(
            quota_request.subject, open_subject
        )  # ตรวจสอบว่า subject ตรงกับ open_subject

    def test_form_is_invalid_without_subject(self):
        # ทดสอบกรณีฟอร์มไม่ถูกต้องเมื่อไม่ได้ส่ง subject มา
        form = RegistrationForm(data={}, student=self.student_user)
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_form_init_without_student(self):
        # ทดสอบการสร้างฟอร์มเมื่อไม่มีการส่ง student มา (student=None)
        form = RegistrationForm()
        self.assertIn(self.open_subject, form.fields["subject"].queryset)
        self.assertNotIn(self.closed_subject, form.fields["subject"].queryset)
