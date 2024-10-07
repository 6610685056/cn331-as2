from django.urls import path
from . import views

urlpatterns = [
    path("", views.subjects, name="subjects"),
    path("<int:subject_id>", views.subject, name="subject"),
    path('register_subject/', views.register_subject, name='register_subject'),
    path('subject_list/', views.subject_list, name='subject_list'),
]
