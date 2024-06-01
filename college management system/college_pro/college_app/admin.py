from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *  # Import your User model


class UserAdminConfig(UserAdmin):
    model = User
    list_display = (
        "email",
        "first_name",
        "is_active",
        "is_hod",
        "is_staff",
        "is_student",
        "is_teacher",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {"fields": ("email", "password", "first_name", "last_name", "username")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "groups",
                    "is_active",
                    "is_staff",
                    "is_hod",
                    "is_student",
                    "is_teacher",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("-date_joined",)


admin.site.register(User, UserAdminConfig)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(SessionYearModel)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedbackStudent)
admin.site.register(FeedbackStaff)
admin.site.register(StudentResult)
