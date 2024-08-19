import django.shortcuts
from django.contrib.auth.decorators import login_required
from app.models import (CustomUser, Routine, Session_year, Staff, Staff_Feedback, Staff_leave,
    Staff_Notification, Student)
from django.contrib import messages
from course.models import Department, Semester
from app.forms import RoutineForm
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
def UPDATE_STUDENT(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')


        user = CustomUser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username= username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()


        student = Student.objects.get(admin =student_id)
        student.address = address
        student.gender = gender

        coures = Semester.objects.get(id =course_id)
        student.course_id = coures

        session_year = Session_year.objects.get(id = session_year_id)
        student.session_year_id = session_year
        student.save()
        messages.success(request,'Record Are Successfully updated !')
        return redirect('view_student')



    return render(request,'Hod/edit_student.html')

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




def create_routine(request):
    # Get the logged-in staff member
    staff = Staff.objects.get(admin=request.user.id)

    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            day = form.cleaned_data.get('day')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')

            # Ensure start_time and end_time are not None
            if start_time is None or end_time is None:
                messages.error(request, "Start time and end time must be provided.")
                return render(request, 'routine/create_routine.html', {'form': form})

            # Check if the teacher is already teaching the same subject on the same day
            existing_routine = Routine.objects.filter(teacher=staff, subject=subject, day=day)
            if existing_routine.exists():
                messages.error(request, "You are already scheduled to teach this subject on the selected day.")
                return render(request, 'routine/create_routine.html', {'form': form})

            # Check for overlapping routines (time conflict)
            overlapping_routine = Routine.objects.filter(
                teacher=staff,
                day=day,
            start_time__lt=end_time,
            end_time__gt=start_time
            )
            if overlapping_routine.exists():
                messages.error(request, "You already have a routine scheduled during the selected time.")
                return render(request, 'routine/create_routine.html', {'form': form})

            try:
                # Create and save the routine
                routine = form.save(commit=False)
                routine.teacher = staff  # Automatically assign the logged-in teacher
                routine.save()
                messages.success(request, "Routine created successfully.")
                return redirect('view_staff')
            except IntegrityError:
                messages.error(request, "There was an error saving your routine. Please try again.")
                return render(request, 'routine/create_routine.html', {'form': form})

    else:
        form = RoutineForm()

    return render(request, 'routine/create_routine.html', {'form': form})


class RoutineCreateView(CreateView):
    model = Routine
    form_class = RoutineForm
    template_name = 'routine/create_routine.html'
    success_url = reverse_lazy('view_staff')

    def form_valid(self, form):
        teacher = form.cleaned_data.get('teacher')
        subject = form.cleaned_data.get('subject')
        day = form.cleaned_data.get('day')
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')

        # Ensure start_time and end_time are not None
        if start_time is None or end_time is None:
            messages.error(self.request, "Start time and end time must be provided.")
            return self.render_to_response(self.get_context_data(form=form))

        # Check if the teacher is already teaching the same subject on the same day
        existing_routine = Routine.objects.filter(teacher=teacher, subject=subject, day=day)
        if existing_routine.exists():
            messages.error(self.request, "This teacher is already scheduled to teach this subject on the selected day.")
            return self.render_to_response(self.get_context_data(form=form))
        
        # Check for overlapping routines (time conflict)
        overlapping_routine = Routine.objects.filter(
            teacher=teacher,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if overlapping_routine.exists():
            messages.error(self.request, "This teacher already has a routine scheduled during the selected time.")
            return self.render_to_response(self.get_context_data(form=form))
        
        try:
            # Try to save the form
            return super().form_valid(form)
        except IntegrityError:
            # Handle the integrity error (unique constraint violation)
            messages.error(self.request, "This teacher already has a routine at the selected time and day.")
            return self.render_to_response(self.get_context_data(form=form))



def check_conflicts(request):
    teacher_id = request.GET.get('teacher')
    day = request.GET.get('day')
    routines = Routine.objects.filter(teacher_id=teacher_id, day=day)
    
    routines_data = [{
        'subject': routine.subject.id,
        'start_time': routine.start_time.strftime('%H:%M'),
        'end_time': routine.end_time.strftime('%H:%M')
    } for routine in routines]

    return JsonResponse(routines_data, safe=False)   

class RoutineUpdateView(UpdateView):
    model = Routine
    form_class = RoutineForm
    template_name = 'routine/create_routine.html'  # Reuse the same template as the create view
    success_url = reverse_lazy('view_staff')

    def form_valid(self, form):
        teacher = form.cleaned_data.get('teacher')
        subject = form.cleaned_data.get('subject')
        day = form.cleaned_data.get('day')
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')

        # Ensure start_time and end_time are not None
        if start_time is None or end_time is None:
            messages.error(self.request, "Start time and end time must be provided.")
            return self.render_to_response(self.get_context_data(form=form))

        # Check if the teacher is already teaching the same subject on the same day
        existing_routine = Routine.objects.filter(
            teacher=teacher, 
            subject=subject, 
            day=day
        ).exclude(pk=self.object.pk)  # Exclude the current instance
        if existing_routine.exists():
            messages.error(self.request, "This teacher is already scheduled to teach this subject on the selected day.")
            return self.render_to_response(self.get_context_data(form=form))
        
        # Check for overlapping routines (time conflict)
        overlapping_routine = Routine.objects.filter(
            teacher=teacher,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(pk=self.object.pk)  # Exclude the current instance
        if overlapping_routine.exists():
            messages.error(self.request, "This teacher already has a routine scheduled during the selected time.")
            return self.render_to_response(self.get_context_data(form=form))
        
        try:
            # Try to save the form
            return super().form_valid(form)
        except IntegrityError:
            # Handle the integrity error (unique constraint violation)
            messages.error(self.request, "This teacher already has a routine at the selected time and day.")
            return self.render_to_response(self.get_context_data(form=form))




def teacher_weekly_routine_view(request, teacher_id):
# Get the teacher object or return a 404 if not found
    teacher = get_object_or_404(Staff, id=teacher_id)
    
    # Initialize a dictionary to store routines by day
    weekly_routines = {day: [] for day, _ in Routine.DAY_CHOICES}
    
    # Get all routines for this teacher
    routines = Routine.objects.filter(teacher=teacher).order_by('day', 'start_time')

    for routine in routines:
        # Check for overlap
        overlap_routine = Routine.objects.filter(
            subject=routine.subject,
        ).exclude(teacher=teacher).first()

        if overlap_routine:
            routine.is_overlapped = True
            routine.overlap_by = overlap_routine.teacher
        else:
            routine.is_overlapped = False
            routine.overlap_by = None

        weekly_routines[routine.day].append(routine)

    return render(request, 'routine/teacher_routine_detail.html', {
        'teacher': teacher,
        'weekly_routines': weekly_routines,
    }
    )
 