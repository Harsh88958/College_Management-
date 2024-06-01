from django.shortcuts import render, redirect, get_object_or_404
from college_app.models import *
from django.http import JsonResponse


# Create your views here.
def staff_dashboard(request):

    return render(request, "staff.html")


def teacher_feedback(request):
    user = request.user
    try:
        staff_id = Staff.objects.get(admin=user)
    except Staff.DoesNotExist:
        return redirect("error_page")  # Redirect to the error page if staff not found

    if request.method == "POST":
        feedback_message = request.POST.get("feedback_message")
        FeedbackStaff.objects.create(
            staff_id=staff_id,
            feedback=feedback_message,
            feedback_reply="",
        )
        return redirect("teacher_feedback")

    feedback_data = FeedbackStaff.objects.all()
    return render(request, "teacher_feedback.html", {"feedback_data": feedback_data})


def teacher_leave(request):
    user = request.user
    try:
        staff_id = Staff.objects.get(admin=user)
    except Staff.DoesNotExist:
        return redirect("error_page")

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")
        LeaveReportStaff.objects.create(
            staff_id=staff_id,
            leave_date=leave_date,
            leave_message=leave_message,
            leave_status="pending",
        )
        return redirect("teacher_leave")
    leave_date = LeaveReportStaff.objects.all()
    return render(request, "teacher_leave.html", {"leave_date": leave_date})


def add_result(request):
    user = request.user
    staff = Staff.objects.get(admin=user)
    subject_obj = Subject.objects.filter(staff_id=staff)
    session_obj = SessionYearModel.objects.all()

    enrolled_students = None
    student_subjects = {}
    student_results = {}

    if request.method == "POST":
        subject_id = request.POST.get("subject")
        session_id = request.POST.get("session")
        print(f"Selected subject_id: {subject_id}, session_id: {session_id}")

        if subject_id and session_id:
            try:
                subject = Subject.objects.get(subject_id=subject_id)
                session = SessionYearModel.objects.get(session_id=session_id)

                enrolled_students = Student.objects.filter(
                    course_id=subject.course_id, session_year_id=session
                )
                print(f"Enrolled students: {enrolled_students}")

                for student in enrolled_students:
                    student_subjects[student.student_id] = Subject.objects.filter(
                        course_id=student.course_id
                    )
                    student_results[student.student_id] = StudentResult.objects.filter(
                        student_id=student, subject_id=subject
                    ).first()

            except Subject.DoesNotExist:
                print(f"Subject with id {subject_id} does not exist.")
            except SessionYearModel.DoesNotExist:
                print(f"Session with id {session_id} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")

    context = {
        "subject_obj": subject_obj,
        "session_obj": session_obj,
        "enrolled_students": enrolled_students,
        "student_subjects": student_subjects,
        "student_results": student_results,
    }
    return render(request, "add_result.html", context)


def save_marks(request, pk):
    if request.method == "POST":
        student_id = pk
        assignment_mark = request.POST.get("assignment_mark")
        exam_mark = request.POST.get("exam_mark")
        subject_id = request.POST.get("subject_id")

        try:
            student = get_object_or_404(Student, pk=student_id)
            subject = get_object_or_404(Subject, pk=subject_id)

            student_result, created = StudentResult.objects.get_or_create(
                student_id=student, subject_id=subject
            )
            student_result.subject_assignment_marks = assignment_mark
            student_result.subject_exam_marks = exam_mark
            student_result.save()

            return redirect("add_result")  # Redirect back to the add_result view
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})
