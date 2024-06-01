from django.shortcuts import render, redirect
from college_app.models import *


# Create your views here.
# Student
def student_dashboard(request):

    return render(request, "student.html")


def leave_student(request):
    user = request.user
    try:
        student = Student.objects.get(admin=user)
    except Student.DoesNotExist:
        return redirect("error_page")  # or handle the error as needed

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")
        LeaveReportStudent.objects.create(
            student_id=student,
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status="pending",
        )
        return redirect("leave_student")

    leave_date = LeaveReportStudent.objects.filter(student_id=student)
    return render(request, "leave.html", {"leave_date": leave_date})


def feedback_student(request):
    user = request.user
    try:
        student = Student.objects.get(admin=user)
    except Student.DoesNotExist:
        return redirect("error_page")  # or handle the error as needed

    if request.method == "POST":
        feedback_message = request.POST.get("feedback_message")
        FeedbackStudent.objects.create(
            student_id=student,
            feedback=feedback_message,
            feedback_reply="",
        )
        return redirect("feedback_student")
    feedback_data = FeedbackStudent.objects.filter(student_id=student)
    return render(request, "feedback.html", {"feedback_data": feedback_data})


def result(request):
    student = Student.objects.get(admin=request.user)
    student_data = StudentResult.objects.filter(student_id=student)

    # Create a list to store the results with the status
    results_with_status = []

    for result in student_data:
        total_marks = result.subject_assignment_marks + result.subject_exam_marks
        status = "Pass" if total_marks >= 33 else "Fail"

        # Append a dictionary with the relevant data
        results_with_status.append(
            {
                "subject_id": result.subject_id,
                "subject_assignment_marks": result.subject_assignment_marks,
                "subject_exam_marks": result.subject_exam_marks,
                "status": status,
            }
        )
    return render(request, "result.html", {"student_data": results_with_status})
