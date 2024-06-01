from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
import uuid, os

# Create your models here.


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a e-mail address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default="", unique=True)

    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    username = models.CharField(max_length=255, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_hod = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.username or self.email.split("@")[0]


class SessionYearModel(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    session_start_year = models.DateField()
    session_last_year = models.DateField()


class Course(models.Model):
    course_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.course_name


def generate_image_path(instance, filename):
    ext = filename.split(".")[-1]
    path = f"media/photos/{instance.student_id}/images/"
    name = f"main.{ext}"
    return os.path.join(path, name)


class Student(models.Model):
    student_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.ImageField(
        upload_to=generate_image_path, blank=True, null=True
    )
    course_id = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
    )
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.admin.username


def generate_staff_image_path(instance, filename):
    ext = filename.split(".")[-1]
    path = f"media/staff_photos/{instance.staff_id}/images/"
    name = f"main.{ext}"
    return os.path.join(path, name)


class Staff(models.Model):
    staff_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    profile_pic = models.ImageField(
        upload_to=generate_staff_image_path, blank=True, null=True
    )
    gender = models.CharField(max_length=50)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.admin.username


class Subject(models.Model):
    subject_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject_name


class Attendance(models.Model):
    attendance_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    attendance_report_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True
    )
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    leave_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    leave_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStudent(models.Model):
    feedback_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    feedback_reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    feedback_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentResult(models.Model):
    result_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Enrollment(models.Model):
    enrollment_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
