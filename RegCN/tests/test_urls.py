from django.test import SimpleTestCase
from django.urls import reverse, resolve
from RegCN import views


class UrlsTest(SimpleTestCase):
    def test_subjects_url(self):
        url = reverse("subjects")
        self.assertEqual(resolve(url).func, views.subjects)

    def test_subject_url(self):
        url = reverse("subject", args=[1])  # จำลองการเรียก URL โดยมี subject_id = 1
        self.assertEqual(resolve(url).func, views.subject)

    def test_register_subject_url(self):
        url = reverse("register_subject")
        self.assertEqual(resolve(url).func, views.register_subject)

    def test_subject_list_url(self):
        url = reverse("subject_list")
        self.assertEqual(resolve(url).func, views.subject_list)

    def test_drop_subject_url(self):
        url = reverse(
            "drop_subject", args=["test-id"]
        )  # จำลองการเรียก URL โดยมี subject_id = "test-id"
        self.assertEqual(resolve(url).func, views.drop_subject)

    def test_home_page_include(self):
        url = reverse("home_page:home")
        self.assertEqual(url, "/")
