import django.shortcuts
from django.contrib.auth.decorators import login_required
from app.models import (CustomUser, Session_year, Staff, Staff_Feedback, Staff_leave,
    Staff_Notification, Student)
from django.contrib import messages
from course.models import Department, Semester

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404

from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q

from django.http import JsonResponse





@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    # course_count = Course.objects.all().count()
    # subject_count= Subject.objects.all().count()


    student_gender_male = Student.objects.filter(gender = 'Male' ).count()
    student_gender_female = Student.objects.filter(gender = 'Female' ).count()


    context = {
        'student_count': student_count,
        'staff_count' : staff_count,
        # 'course_count' : course_count,
        # 'subject_count' : subject_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,


    }
    return render(request,'Hod/home.html',context)




@login_required(login_url='/')

def ADD_STUDENT(request):
    semesters = Semester.objects.all()
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        semester_id = request.POST.get('semester_id')
        roll_no = request.POST.get('roll_no')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            semester = Semester.objects.get(id=semester_id)

            student = Student(
                admin=user,
                address=address,
                semester=semester,
                gender=gender,
                roll_no=roll_no,
            )
            student.save()
            messages.success(request, user.first_name + " " + user.last_name + " has been successfully added!")
            return redirect('view_student')

    context = {
        'semesters': semesters,
    }

    return render(request, 'Hod/add_student.html', context)





@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student':student,
    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Semester.objects.all()
    session_year = Session_year.objects.all()

    context = {
        'student':student,
        'course':course,
        'session_year':session_year,
    }
    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = get_object_or_404(Student, id=id)
    semesters = Semester.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        semester_id = request.POST.get('semester_id')
        roll_no = request.POST.get('roll_no')

        # Update the related CustomUser object
        user = student.admin
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password:
            user.set_password(password)
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()

        # Update the Student object
        student.address = address
        student.gender = gender
        student.roll_no = roll_no

        if semester_id:
            semester = get_object_or_404(Semester, id=semester_id)
            student.semester = semester

        student.save()
        messages.success(request, f'{user.first_name} {user.last_name} has been successfully updated!')
        return redirect('view_student')

    context = {
        'student': student,
        'semesters': semesters,
    }

    return render(request, 'Hod/edit_student.html', context)


@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request,'Record Are Succesfully Deleted')
    return redirect('view_student')












@login_required(login_url='/')
def ADD_STAFF(request):
    departments = Department.objects.all()  # Fetch all departments
    rank_choices = Staff.RANK_CHOICES
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department')
        credit_access = request.POST.get('credit_access')
        rank = request.POST.get('rank')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_staff')
        else:
            # Create the CustomUser instance
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            # Fetch the department instance
            department = Department.objects.get(id=department_id)

            # Create the Staff instance
            staff = Staff(
                admin=user,
                first_name=first_name,
                last_name=last_name,
                address=address,
                gender=gender,
                department=department,
                rank=rank,
                credit_access=credit_access,
            )
            staff.save()
            messages.success(request, f"{user.first_name} {user.last_name} has been successfully added!")
            return redirect('view_staff')

    context = {
        'departments': departments,
        'rank_choices': rank_choices,
    }

    return render(request, 'Hod/add_staff.html', context)



@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)

@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = get_object_or_404(Staff, id=id)
    departments = Department.objects.all()  # Fetch all departments
    rank_choices = Staff.RANK_CHOICES

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department')
        rank = request.POST.get('rank')
        credit_access = request.POST.get('credit_access')

        if CustomUser.objects.filter(email=email).exclude(id=staff.admin.id).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('edit_staff', id=id)
        if CustomUser.objects.filter(username=username).exclude(id=staff.admin.id).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('edit_staff', id=id)
        else:
            user = staff.admin
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.profile_pic = profile_pic if profile_pic else user.profile_pic
            if password:
                user.set_password(password)
            user.save()

            # Update the staff details
            staff.first_name = first_name
            staff.last_name = last_name
            staff.address = address
            staff.gender = gender
            staff.department = Department.objects.get(id=department_id)
            staff.rank = rank
            staff.credit_access = credit_access
            staff.save()

            messages.success(request, f'{user.first_name} {user.last_name} has been successfully updated!')
            return redirect('view_staff')

    context = {
        'staff': staff,
        'departments': departments,
        'rank_choices': rank_choices,
    }

    return render(request, 'Hod/edit_staff.html', context)

@login_required(login_url='/')
def DELETE_STAFF(request, id):
    staff = get_object_or_404(CustomUser, id=id)
    staff.delete()
    messages.success(request, 'Record has been deleted successfully.')
    return redirect('staff_list')  # Redirect to the list view after successful deletion






@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_start')

        session = Session_year(
            session_start =session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Successfuly Created')
        return redirect('add_session')
    return render(request,'Hod/add_session.html')

@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_year.objects.all()

    context = {
        'session': session,
    }
    return render(request,'Hod/view_session.html',context)

@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session = Session_year.objects.filter(id= id)

    context ={
        'session': session,
    }
    return render(request,'Hod/edit_session.html',context)

@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_year(
            id = session_id,
            session_start =session_year_start,
            session_end = session_year_end

        )
        session.save()
        messages.success(request,'Session Are successfuly update')
        return redirect('view_session')

@login_required(login_url='/')
def DELETE_SESSION(request,id):
    session = Session_year.objects.get(id= id)
    session.delete()
    messages.success(request,'Session Are Sueccessfully Delete')
    return redirect('view_session')


def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_nofification = Staff_Notification.objects.all().order_by('-id')[0:5]

    context ={
        'staff':staff,
        'see_nofification' : see_nofification,
    }
    return render(request,'Hod/staff_notification.html',context)


def SAVE_NOTIFICATION(request):
    if request.method == 'POST':
        staff_id =request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,

        )
        notification.save()
        messages.success(request,'notification Are Successfuly send')
        return redirect('staff_send_notification')


def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_leave.objects.all()

    context ={
        "staff_leave" : staff_leave,

    }
    return render(request,'Hod/staff_leave.html',context)


def STAFF_APPROVE_LEAVE(request,id):
    leave = Staff_leave.objects.get(id =id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')


def STAFF_DISAPPROVE_LEAVE(request,id):
    leave = Staff_leave.objects.get(id = id)
    leave.status =2
    leave.save()
    return redirect('staff_leave_view')


def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()

    context = {
        'feedback' : feedback,
    }
    return render (request, 'Hod/staff_feedback.html',context)


def STAFF_FEEDBACK_REPLY(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()

        return redirect('staff_feedback')



