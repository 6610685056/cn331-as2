from django import forms
from .models import Subject, QuotaRequest

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = QuotaRequest
        fields = ['subject']

    def __init__(self, *args, **kwargs):
        # รับ request ผ่าน kwargs เพื่อให้นักเรียนแต่ละคนสามารถลงทะเบียนเรียนได้
        self.student = kwargs.pop('student', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # กรองวิชาเฉพาะที่เปิดอยู่เท่านั้น
        self.fields['subject'].queryset = Subject.objects.filter(subject_is_open=True)

    def save(self, commit=True):
        quota_request = super(RegistrationForm, self).save(commit=False)
        if self.student:
            quota_request.student = self.student  # กำหนดนักเรียนที่ทำการลงทะเบียน
        if commit:
            quota_request.save()
        return quota_request