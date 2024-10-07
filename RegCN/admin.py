from django.contrib import admin
from .models import Subject, QuotaRequest

# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title','subject_id','subject_is_open']
    search_fields = ['title','subject_id']
    list_filter = ['subject_id']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(QuotaRequest)