from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout


def hod_dashboard(request):
    return render(request, "hod.html")


def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        student_email = request.POST.get("student_email")
        gender = request.POST.get("gender")
        profile_pic = request.FILES.get("profile_pic")
        course_id = request.POST.get("course")
        session_year_id = request.POST.get("session_year")
        address = request.POST.get("address")
        username = f"{first_name} {last_name}"
        user_obj = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=student_email,
            is_student=True,
        )
        user_obj.set_password(password)
        user_obj.save()
        student = Student.objects.create(
            admin=user_obj,
            gender=gender,
            profile_pic=profile_pic,
            course_id_id=course_id,
            session_year_id_id=session_year_id,
            address=address,
        )
        return redirect("add_student")
    course_data = Course.objects.all()
    session_data = SessionYearModel.objects.all()
    return render(
        request,
        "addstudent.html",
        {"course_data": course_data, "session_data": session_data},
    )


def add_staff(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        staff_email = request.POST.get("staff_email")
        gender = request.POST.get("gender")
        profile_pic = request.FILES.get("profile_pic")
        address = request.POST.get("address")
        # Create a User object
        username = f"{first_name} {last_name}"
        user_obj = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=staff_email,
            is_staff=True,
        )

        # Set password for the user
        user_obj.set_password(password)
        user_obj.save()
        staff = Staff.objects.create(
            admin=user_obj,
            gender=gender,
            profile_pic=profile_pic,
            address=address,
        )
        return redirect("add_staff")
    return render(request, "addstaff.html")


def add_course(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        Course.objects.create(
            course_name=course_name,
        )
        return redirect("add_course")
    return render(request, "addcourse.html")


def add_session(request):
    if request.method == "POST":
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        SessionYearModel.objects.create(
            session_start_year=session_start,
            session_last_year=session_end,
        )
        return redirect("add_session")
    return render(request, "addsession.html")


def add_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        course = request.POST.get("course")
        staff = request.POST.get("staff")
        Subject.objects.create(
            subject_name=subject_name, course_id_id=course, staff_id_id=staff
        )
    course_data = Course.objects.all()
    staff_data = Staff.objects.all()
    return render(
        request,
        "addsubject.html",
        {"course_data": course_data, "staff_data": staff_data},
    )


def manage_student(request):
    student_obj = Student.objects.all()
    return render(request, "managestudent.html", {"student_obj": student_obj})


def manage_staff(request):
    staff_obj = Staff.objects.all()
    return render(request, "managestaff.html", {"staff_obj": staff_obj})


def manage_session(request):
    session_obj = SessionYearModel.objects.all()
    return render(request, "managesession.html", {"session_obj": session_obj})


def manage_subject(request):
    subject_obj = Subject.objects.all()
    return render(request, "managesubject.html", {"subject_obj": subject_obj})


def manage_course(request):
    course_obj = Course.objects.all()
    course_edit = None
    if "edit_id" in request.session:
        try:
            course_edit = Course.objects.get(course_id=request.session["edit_id"])
        except Course.DoesNotExist:
            pass
        del request.session["edit_id"]
    return render(
        request,
        "managecourse.html",
        {"course_obj": course_obj, "course_edit": course_edit},
    )


def manage_subject(request):
    subject_obj = Subject.objects.all()
    subject_edit = None
    if "edit_id" in request.session:
        try:
            subject_edit = Subject.objects.get(subject_id=request.session["edit_id"])
        except Subject.DoesNotExist:
            pass
        del request.session["edit_id"]
    course_data = Course.objects.all()
    staff_data = Staff.objects.all()
    return render(
        request,
        "managesubject.html",
        {
            "subject_obj": subject_obj,
            "subject_edit": subject_edit,
            "course_data": course_data,
            "staff_data": staff_data,
        },
    )


def manage_session(request):
    session_obj = SessionYearModel.objects.all()
    session_edit = None
    if "edit_id" in request.session:
        try:
            session_edit = SessionYearModel.objects.get(
                session_id=request.session["edit_id"]
            )
        except SessionYearModel.DoesNotExist:
            pass
        del request.session["edit_id"]
    return render(
        request,
        "managesession.html",
        {"session_obj": session_obj, "session_edit": session_edit},
    )


def edit_course(request, pk):
    if pk is not None:
        request.session["edit_id"] = pk
        return redirect("manage_course")
    else:
        pass


def edit_session(request, pk):
    if pk is not None:
        request.session["edit_id"] = pk
        return redirect("manage_session")
    else:
        pass


def edit_subject(request, pk):
    if pk is not None:
        request.session["edit_id"] = pk
        return redirect("manage_subject")
    else:
        pass


def save_course(request, pk):
    if request.method == "POST":
        course_edit = Course.objects.get(course_id=pk)
        course_name = request.POST.get("course_name")
        course_edit.course_name = course_name
        course_edit.save()
    return redirect("manage_course")


def save_session(request, pk):
    if request.method == "POST":
        session_edit = SessionYearModel.objects.get(session_id=pk)
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        if session_start:
            session_edit.session_start_year = session_start
            session_edit.save()
        elif session_end:
            session_edit.session_last_year = session_end
            session_edit.save()
    return redirect("manage_session")


def save_subject(request, pk):
    if request.method == "POST":
        subject_edit = Subject.objects.get(subject_id=pk)
        subject_name = request.POST.get("subject_name")
        course = request.POST.get("course")
        staff = request.POST.get("staff")
        if subject_name:
            subject_edit.subject_name = subject_name
            subject_edit.save()
        elif course:
            subject_edit.course_id_id = course
            subject_edit.save()
        elif staff:
            subject_edit.staff_id_id = staff
            subject_edit.save()
    return redirect("manage_subject")


def delete_course(self, pk):
    Course.objects.get(course_id=pk).delete()
    return redirect("manage_course")


def delete_session(self, pk):
    SessionYearModel.objects.get(session_id=pk).delete()
    return redirect("manage_session")


def delete_subject(self, pk):
    Subject.objects.get(subject_id=pk).delete()
    return redirect("manage_subject")


# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            user_obj = User.objects.get(email=user)
            login(request, user)
            if user_obj.is_hod and user_obj.is_staff:
                return redirect("hod")
            elif user_obj.is_staff and user_obj.is_teacher:
                return redirect("staff")
            elif user_obj.is_student and user_obj.is_staff:
                return redirect("student")
        else:
            return redirect("login")
    return render(request, "login.html")


def custom_logout(request):
    logout(request)  # type: ignore
    return redirect("/")


def student_feedback(request):
    leave_obj = FeedbackStudent.objects.all()
    leave_edit = None
    if "edit_id" in request.session:
        try:
            leave_edit = FeedbackStudent.objects.get(
                feedback_id=request.session["edit_id"]
            )
        except FeedbackStudent.DoesNotExist:
            pass
        del request.session["edit_id"]
    return render(
        request,
        "studentfeedback.html",
        {"leave_obj": leave_obj, "leave_edit": leave_edit},
    )


def staff_feedback(request):
    feed_obj = FeedbackStaff.objects.all()
    feed_edit = None
    if "edit_id" in request.session:
        try:
            feed_edit = FeedbackStaff.objects.get(
                feedback_id=request.session["edit_id"]
            )
        except FeedbackStaff.DoesNotExist:
            pass
        del request.session["edit_id"]
    return render(
        request,
        "staff_feedback.html",
        {"feed_obj": feed_obj, "feed_edit": feed_edit},
    )


def edit_feedback(request, pk):
    if pk is not None:
        request.session["edit_id"] = pk
        return redirect("staff_feedback")
    else:
        pass


def edit_leave(request, pk):
    if pk is not None:
        request.session["edit_id"] = pk
        return redirect("student_feedback")
    else:
        pass


def save_feedback(request, pk):
    if request.method == "POST":
        leave_edit = FeedbackStaff.objects.get(feedback_id=pk)
        feedback_reply = request.POST.get("feedback_reply")
        leave_edit.feedback_reply = feedback_reply
        leave_edit.save()
    return redirect("staff_feedback")


def save_leave(request, pk):
    if request.method == "POST":
        leave_edit = FeedbackStudent.objects.get(feedback_id=pk)
        feedback_reply = request.POST.get("feedback_reply")
        leave_edit.feedback_reply = feedback_reply
        leave_edit.save()
    return redirect("student_feedback")


def student_leave(request):
    feedback_data = LeaveReportStudent.objects.all()
    return render(request, "studentleave.html", {"feedback_data": feedback_data})


def student_leave_accept(request, pk):
    leave_data = LeaveReportStudent.objects.get(leave_id=pk)
    leave_data.leave_status = "Accepted"
    leave_data.save()
    return redirect("student_leave")


def student_leave_reject(request, pk):
    leave_data = LeaveReportStudent.objects.get(leave_id=pk)
    leave_data.leave_status = "Rejected"
    leave_data.save()
    return redirect("student_leave")


def staff_leave(request):
    feedback_data = LeaveReportStaff.objects.all()
    return render(request, "staff_leave.html", {"feedback_data": feedback_data})


def staff_leave_accept(request, pk):
    leave_data = LeaveReportStaff.objects.get(leave_id=pk)
    leave_data.leave_status = "Accepted"
    leave_data.save()
    return redirect("staff_leave")


def staff_leave_reject(request, pk):
    leave_data = LeaveReportStaff.objects.get(leave_id=pk)
    leave_data.leave_status = "Rejected"
    leave_data.save()
    return redirect("staff_leave")
