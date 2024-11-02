from django.test import TestCase
from django.contrib.admin.sites import site
from RegCN.models import Subject, QuotaRequest

class AdminTestCase(TestCase):
    def test_subject_registered(self):
        # ตรวจสอบว่าโมเดล Subject ถูกลงทะเบียนใน admin
        self.assertIn(Subject, site._registry)

    def test_quota_request_registered(self):
        # ตรวจสอบว่าโมเดล QuotaRequest ถูกลงทะเบียนใน admin
        self.assertIn(QuotaRequest, site._registry)
