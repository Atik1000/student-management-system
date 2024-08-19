import django.http
from django.shortcuts import render,redirect
from app.models import Staff, Staff_Feedback, Staff_leave, Staff_Notification, TeacherSubjectChoice
from django.contrib import messages
from Student_Management_systems.Hod_views import SAVE_NOTIFICATION

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
    



from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from app.forms import TeacherSubjectChoiceForm
from course.models import Semester, SemesterType, Subject

from django.http import JsonResponse


class TeacherSubjectChoiceCreateView(CreateView):
    model = TeacherSubjectChoice
    form_class = TeacherSubjectChoiceForm
    template_name = 'subject/teacher_subject_choice_form.html'
    success_url = reverse_lazy('subject_choice_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['staff'] = self.request.user.staff
        return kwargs

class TeacherSubjectChoiceUpdateView(UpdateView):
    model = TeacherSubjectChoice
    form_class = TeacherSubjectChoiceForm
    template_name = 'subject/teacher_subject_choice_form.html'
    success_url = reverse_lazy('subject_choice_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['staff'] = self.request.user.staff
        return kwargs



def filter_semester_types(request):
    department_id = request.GET.get('department_id')
    semester_types = SemesterType.objects.filter(type_semesters__department_id=department_id).distinct()
    options = '<option value="">---------</option>'
    for semester_type in semester_types:
        options += f'<option value="{semester_type.id}">{semester_type.get_semester_type_name_display()}</option>'
    return JsonResponse({'options': options})

def filter_semesters(request):
    semester_type_id = request.GET.get('semester_type_id')
    department_id = request.GET.get('department_id')
    semesters = Semester.objects.filter(semester_type_id=semester_type_id, department_id=department_id).distinct()
    options = '<option value="">---------</option>'
    for semester in semesters:
        options += f'<option value="{semester.id}">{semester.name}</option>'
    return JsonResponse({'options': options})

def filter_subjects(request):
    semester_id = request.GET.get('semester_id')
    department_id = request.GET.get('department_id')
    subjects = Subject.objects.filter(semester_id=semester_id, department_id=department_id).distinct()
    options = '<option value="">---------</option>'
    for subject in subjects:
        options += f'<option value="{subject.id}">{subject.sub_name}</option>'
    return JsonResponse({'options': options})