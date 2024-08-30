from django.urls import path
from .views import (department_list_view,
    DepartmentCreateView, DepartmentListView, DepartmentUpdateView, filter_departments,
    filter_semesters, program_list_view, ProgramCreateView, ProgramListView, semester_list_view,
    semester_type_detail, semester_type_list_view, SemesterCreateView,
    SemesterListView, SemesterUpdateView, subject_list_view, SubjectCreateView, SubjectListView,
    SubjectUpdateView)

urlpatterns = [
    # Program URLs
    path('programs/', ProgramListView.as_view(), name='program_list'),
    path('programs/create/', ProgramCreateView.as_view(), name='program_create'),
    
    # Department URLs
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/update/', DepartmentUpdateView.as_view(), name='department_update'),
    
    # Semester URLs
    path('semesters/', SemesterListView.as_view(), name='semester_list'),
    path('semesters/create/', SemesterCreateView.as_view(), name='semester_create'),
    path('semesters/<int:pk>/update/', SemesterUpdateView.as_view(), name='semester_update'),
    path('filter-departments/', filter_departments, name='filter_departments'),


    # Subject Urls
    path('subject', SubjectListView.as_view(), name='subject_list'),
    path('subject/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subject/<int:pk>/edit/', SubjectUpdateView.as_view(), name='subject_update'),
    path('filter-semesters/', filter_semesters, name='filter_semesters'),

    # curriculam 
    path('curriculam_programs/',program_list_view, name='program_list_curriculam'),
    path('curriculam_programs/<int:program_id>/departments/', department_list_view, name='department_list_curriculam'),
    path('curriculam_departments/<int:department_id>/semester-types/',semester_type_list_view, name='semester_type_list_curriculam'),
    path('curriculam_departments/<int:department_id>/semester-types/<int:semester_type_id>/semesters/',semester_list_view, name='semester_list_curriculam'),
    path('curriculam_semesters/<int:semester_id>/subjects/',subject_list_view, name='subject_list_curriculam'),
    path('semester-type/<int:semester_type_id>/', semester_type_detail, name='semester_type_detail'),



]
