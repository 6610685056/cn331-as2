from django.urls import path
from . import views

urlpatterns = [
    path("", views.subjects, name="subjects"),
    path("<int:subject_id>", views.subject, name="subject"),
]
