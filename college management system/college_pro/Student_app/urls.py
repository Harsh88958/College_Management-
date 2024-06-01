from django.urls import path
from .views import *

urlpatterns = [
    path("", student_dashboard, name="student"),
    path("leave_student/", leave_student, name="leave_student"),
    path("result/", result, name="result"),
    path("feedback_student/", feedback_student, name="feedback_student"),
]
