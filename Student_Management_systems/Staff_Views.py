import django.http
from django.shortcuts import render,redirect
from app.models import (Intake, Staff, Staff_Feedback, Staff_leave, Staff_Notification,
    TeacherSubjectChoice)
from django.contrib import messages
from Student_Management_systems.Hod_views import SAVE_NOTIFICATION


from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from app.forms import TeacherSubjectChoiceForm
from course.models import Semester, SemesterType, Subject

from django.http import JsonResponse



def HOME(request):
    return render(request,'Staff/home.html')



def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin=request.user.id)
    notifications = []
    
    for i in staff:
        staff_id = i.id
        notification = Staff_Notification.objects.filter(staff_id=staff_id)
        notifications.extend(notification)
    
    context = {
        'notification': notifications,
    }
    
    return render(request, 'Staff/notification.html', context)



def STAFF_NOTIFICATION_MARK_AS_DONE(request,status):
    notification =Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notification')


def STAFF_APPLY_LEAVE(request):

    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id = staff_id)
        context = {
            'staff_leave_history' : staff_leave_history,
        }


    return render(request,'Staff/apply_leave.html',context)


def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == 'POST':
        leave_date =request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        staff = Staff.objects.get(admin = request.user.id )

        leave = Staff_leave(
            staff_id = staff,
            date = leave_date,
            message = leave_message,

        )
        messages.success(request,"Staff Leave Successfuly Send")
        leave.save()


        return redirect('staff_apply_leave')


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin = request.user.id)

    feedback_history = Staff_Feedback.objects.filter(staff_id =staff_id)

    context = {
     'feedback_history' : feedback_history,

    }
    return render(request,'Staff/feedback.html',context)

def STAFF_FEEDBACK_SAVE(request):
    if  request.method == 'POST':
        feedback = request.POST.get('feedback')
        staff = Staff.objects.get(admin = request.user.id )
        feedback=Staff_Feedback(


            staff_id = staff,
            feedback = feedback,
            feedback_reply = " ",
        )
        feedback.save()
        return redirect('staff-feedback') 
    



class TeacherSubjectChoiceCreateView(CreateView):
    model = TeacherSubjectChoice
    form_class = TeacherSubjectChoiceForm
    template_name = 'subject/teacher_subject_choice_form.html'  # Adjust the template name as needed

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['staff'] = self.request.user.staff
        return kwargs

    def form_valid(self, form):
        form.instance.staff = self.request.user.staff
        return super().form_valid(form)
    

class TeacherSubjectChoiceUpdateView(UpdateView):
    model = TeacherSubjectChoice
    form_class = TeacherSubjectChoiceForm
    template_name = 'subject/teacher_subject_choice_form.html'
    success_url = reverse_lazy('subject_choice_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['staff'] = self.request.user.staff
        return kwargs


def load_semesters(request):
    department_id = request.GET.get('department')
    semester_type_id = request.GET.get('semester_type')

    semesters = Semester.objects.filter(department_id=department_id, semester_type_id=semester_type_id)
    
    return JsonResponse({'semesters': list(semesters.values('id', 'name'))})


def load_batches(request):
    semester_id = request.GET.get('semester')
    if semester_id:
        batches = Intake.objects.filter(sem_name=semester_id)
        return JsonResponse({'batches': list(batches.values('id', 'name'))})
    return JsonResponse({'batches': []})


def load_subjects(request):
    semester_id = request.GET.get('semester')
    
    subjects = Subject.objects.filter(semester_id=semester_id)
    
    return JsonResponse({'subjects': list(subjects.values('id', 'sub_name'))})
