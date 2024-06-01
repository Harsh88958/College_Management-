from django.urls import path
from .views import *

urlpatterns = [
    path("", staff_dashboard, name="staff"),
    path("teacher_feedback/", teacher_feedback, name="teacher_feedback"),
    path("teacher_leave/", teacher_leave, name="teacher_leave"),
    path("add_result/", add_result, name="add_result"),
    path("save_marks/<str:pk>/", save_marks, name="save_marks"),
]
