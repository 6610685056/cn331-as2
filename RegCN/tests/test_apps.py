from django.apps import apps
from django.test import TestCase
from RegCN.apps import RegcnConfig  # เปลี่ยนเป็นชื่อแอปจริง

class AppConfigTest(TestCase):
    def test_app_name(self):
        self.assertEqual(RegcnConfig.name, 'RegCN')  # เปลี่ยน 'myapp' ให้ตรงกับชื่อแอปจริง
        self.assertEqual(apps.get_app_config('RegCN').name, 'RegCN')
