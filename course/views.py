from django.urls import reverse_lazy
from .models import  Department, Program, Semester, SemesterType, Subject
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import ProgramForm, DepartmentForm, SemesterForm,SubjectForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.db.models import Sum, Case, When, IntegerField, F, Value
from django.db.models.functions import Coalesce

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'course/program_form.html'
    success_url = reverse_lazy('program_list')


class ProgramListView(ListView):
    model = Program
    template_name = 'course/program_list.html'
    context_object_name = 'programs'



# Department Views
class DepartmentListView(ListView):
    model = Department
    template_name = 'course/department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'course/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'course/department_form.html'
    success_url = reverse_lazy('department_list')



# Semester Views
class SemesterListView(ListView):
    model = Semester
    template_name = 'course/semester_list.html'
    context_object_name = 'semesters'

class SemesterCreateView(CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'course/semester_form.html'
    success_url = reverse_lazy('semester_list')


def filter_departments(request):
    program_id = request.GET.get('program_id')
    departments = Department.objects.filter(program_id=program_id)
    options = '<option value="">---------</option>'
    for department in departments:
        options += f'<option value="{department.id}">{department.dept_name}</option>'
    return JsonResponse({'options': options})

class SemesterUpdateView(UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'course/semester_form.html'
    success_url = reverse_lazy('semester_list')




class SubjectListView(ListView):
    model = Subject
    template_name = 'course/subject_list.html'
    context_object_name = 'subjects'


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'course/subject_form.html'
    success_url = reverse_lazy('subject_list')



def filter_semesters(request):
    semester_type_id = request.GET.get('semester_type_id')
    print('Received Semester Type ID:', semester_type_id)  # Debugging line

    if semester_type_id:
        try:
            # Filter semesters by the provided semester_type_id
            semesters = Semester.objects.filter(semester_type_id=semester_type_id).order_by('name')
            print('Found Semesters:', list(semesters))  # Debugging line
        except ValueError:
            # Handle case if semester_type_id is invalid
            semesters = Semester.objects.none()
    else:
        semesters = Semester.objects.none()

    options = '<option value="">---------</option>'
    for semester in semesters:
        options += f'<option value="{semester.id}">{semester.name}</option>'
    
    print('Returning Options:', options)  # Debugging line
    return JsonResponse({'options': options})



class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'course/subject_form.html'
    success_url = reverse_lazy('subject_list')


# Curriculam 

def program_list_view(request):
    programs = Program.objects.all()
    return render(request, 'curriculum/program_list.html', {'programs': programs})

def department_list_view(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    departments = Department.objects.filter(program=program)
    return render(request, 'curriculum/department_list.html', {'program': program, 'departments': departments})

def semester_type_list_view(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    semester_types = SemesterType.objects.filter(type_semesters__department=department).distinct()
    return render(request, 'curriculum/semester_type_list.html', {'department': department, 'semester_types': semester_types})

def semester_list_view(request, department_id, semester_type_id):
    department = get_object_or_404(Department, id=department_id)
    semester_type = get_object_or_404(SemesterType, id=semester_type_id)
    semesters = Semester.objects.filter(department=department, semester_type=semester_type)
    return render(request, 'curriculum/semester_list.html', {'department': department, 'semester_type': semester_type, 'semesters': semesters})

def subject_list_view(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    return render(request, 'curriculum/subject_list.html', {'semester': semester, 'subjects': subjects})



def semester_type_detail(request, semester_type_id):
    semester_type = get_object_or_404(SemesterType, id=semester_type_id)
    semesters = Semester.objects.filter(semester_type=semester_type)
    
    context = {
        'semester_type': semester_type,
        'semesters': semesters,
    }
    return render(request, 'curriculum/semester_type_details.html', context)