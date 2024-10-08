import django.http
from django.shortcuts import render,redirect
from app.models import ( Staff, Staff_Feedback, Staff_leave, Staff_Notification,
    TeacherSubjectChoice)
from django.contrib import messages
from Student_Management_systems.Hod_views import SAVE_NOTIFICATION
from django.db.models import Sum

from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from app.forms import TeacherSubjectChoiceForm
from course.models import Semester, SemesterType, Subject

from django.http import JsonResponse


def HOME(request):
    return render(request, 'Staff/home.html')


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
    template_name = 'subject/teacher_subject_choice_form.html'
    success_url = reverse_lazy('teacher-subject-choice-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['staff'] = self.request.user.staff
        return kwargs

    def form_valid(self, form):
        staff = self.request.user.staff
        form.instance.staff = staff

        # Retrieve the dynamic credit limit from the staff's `credit_access` field
        credit_limit = staff.credit_access or 20  # Default to 20 if not set

        # Check current total credits
        current_total_credits = TeacherSubjectChoice.objects.filter(
            staff=staff
        ).aggregate(total=Sum('subject__credit'))['total'] or 0

        new_total_credits = current_total_credits + form.instance.subject.credit
        if new_total_credits > credit_limit:
            form.add_error('subject', f"Adding this subject will exceed your credit limit of {credit_limit} credits. Your current total is {current_total_credits} credits.")
            return self.form_invalid(form)

        # Check for higher-ranked staff
        higher_ranks = ['CH', 'AP', 'AS', 'LE']
        staff_rank_index = higher_ranks.index(staff.rank)
        higher_ranks = higher_ranks[:staff_rank_index]

        if TeacherSubjectChoice.objects.filter(
            subject=form.instance.subject,
            staff__rank__in=higher_ranks
        ).exists():
            form.add_error('subject', 'This subject has already been selected by a higher-ranked staff member.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Render the form with errors
        return self.render_to_response(self.get_context_data(form=form))


class TeacherSubjectChoiceUpdateView(UpdateView):
    model = TeacherSubjectChoice
    form_class = TeacherSubjectChoiceForm
    template_name = 'subject/teacher_subject_choice_form.html'
    success_url = reverse_lazy('teacher-subject-choice-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['staff'] = self.request.user.staff
        return kwargs

    def form_valid(self, form):
        form.instance.staff = self.request.user.staff

        # Check if a higher-ranked teacher has selected this subject
        higher_ranks = ['CH', 'AP', 'AS','LE']
        staff_rank_index = higher_ranks.index(self.request.user.staff.rank)
        higher_ranks = higher_ranks[:staff_rank_index]

        if TeacherSubjectChoice.objects.filter(
            subject=form.instance.subject,
            staff__rank__in=higher_ranks
        ).exists():
            form.add_error('subject', 'This subject has already been selected by a higher-ranked staff member.')
            return self.form_invalid(form)

        return super().form_valid(form)



def load_semesters(request):
    department_id = request.GET.get('department')
    semester_type_id = request.GET.get('semester_type')

    semesters = Semester.objects.filter(department_id=department_id, semester_type_id=semester_type_id)
    
    return JsonResponse({'semesters': list(semesters.values('id', 'name'))})



def load_subjects(request):
    semester_id = request.GET.get('semester')
    
    subjects = Subject.objects.filter(semester_id=semester_id)
    
    return JsonResponse({'subjects': list(subjects.values('id', 'sub_name'))})


def ajax_get_total_credits(request):
    staff_id = request.GET.get('staff_id')
    total_credits = TeacherSubjectChoice.objects.filter(staff_id=staff_id).aggregate(total=Sum('subject__credit'))['total'] or 0
    return JsonResponse({'total_credits': total_credits})

from django.contrib.auth.decorators import login_required




@login_required  # Ensure that only logged-in users can access this view
def teacher_subject_choice_list(request):
    teacher_subject_choices = TeacherSubjectChoice.objects.filter(staff=request.user.staff)  # Filter choices by the logged-in staff member
    total_credits = teacher_subject_choices.aggregate(total=Sum('subject__credit'))['total'] or 0


    context = {
        'teacher_subject_choices': teacher_subject_choices,
        'total_credits': total_credits,

    }
    return render(request, 'subject/single_teacher_subject_list.html', context)  # Replace 'your_app' with your actual app name


class TeacherSubjectChoiceListView(ListView):
    model = TeacherSubjectChoice
    template_name = 'subject/teacher_subject_choice_list.html'  # Updated with correct template name
    context_object_name = 'subject_choices'
    
    def get_queryset(self):
        # Get the teacher based on the primary key (pk) in the URL
        teacher = get_object_or_404(Staff, pk=self.kwargs['pk'])
        # Filter the TeacherSubjectChoice by the teacher
        return TeacherSubjectChoice.objects.filter(staff=teacher)

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        # Add the teacher object to the context
        context['teacher'] = get_object_or_404(Staff, pk=self.kwargs['pk'])
        # Calculate the total credits
        total_credits = self.get_queryset().aggregate(Sum('subject__credit'))['subject__credit__sum'] or 0
        context['total_credits'] = total_credits
        return context


def pdf_view(request, pk):
    # Fetch the teacher and their subject choices
    teacher = get_object_or_404(Staff, pk=pk)
    subject_choices = TeacherSubjectChoice.objects.filter(staff=teacher)
    
    # Generate the HTML content
    html_string = render_to_string('subject/staff_routine_pdf.html', {
        'subject_choices': subject_choices,
        'teacher': teacher,
        'total_credits': subject_choices.aggregate(Sum('subject__credit'))['subject__credit__sum'] or 0
    })
    
    # Create the PDF
    pdf = HTML(string=html_string).write_pdf()
    
    # Return the PDF as an HTTP response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="subject_choices_{pk}.pdf"'
    return response


def check_higher_rank_completion(request):
    staff_id = request.GET.get('staff_id')
    semester_id = request.GET.get('semester_id')

    # Fetch the current staff member
    staff = Staff.objects.get(id=staff_id)

    # Define higher ranks
    higher_ranks = ['CH', 'AP', 'AS', 'LE']
    higher_ranks = higher_ranks[:higher_ranks.index(staff.rank)]

    for rank in higher_ranks:
        higher_rank_staff = Staff.objects.filter(rank=rank)
        for higher_staff in higher_rank_staff:
            total_credits = TeacherSubjectChoice.objects.filter(
                staff=higher_staff,
                semester_id=semester_id
            ).aggregate(total=Sum('subject__credit'))['total'] or 0

            # If any higher-ranked teacher has less than 20 credits, return a blocking message
            if total_credits < 20:
                return JsonResponse({
                    'can_select': False,
                    'message': f"A higher-ranked teacher ({higher_staff.rank}) has not completed their 20 credit selection. You cannot select a subject until they finish."
                })

    # If no blocking conditions are found, allow the selection
    return JsonResponse({'can_select': True})