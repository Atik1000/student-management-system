
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Student_Management_systems.Staff_Views import ( load_semesters, load_subjects,
    STAFF_FEEDBACK, teacher_subject_choice_list, TeacherSubjectChoiceCreateView,
    TeacherSubjectChoiceUpdateView,TeacherSubjectChoiceListView,check_higher_rank_completion,ajax_get_total_credits,pdf_view)

from .import views,Hod_views,Staff_Views,Student_Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='base'),

    #Login path
    path('',views.LOGIN,name='login'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('doLogout',views.doLogout,name='logout'),
    path('profile/update',views.PROFILE_UPDATE,name= 'profile_update'),

    # profile Update
    path('profile',views.PROFILE, name='profile'),

# HOD Panel url
    path('Hod/Home',Hod_views.HOME,name='hod_home'),
    path('Hod/Student/Add',Hod_views.ADD_STUDENT,name='add_student'),
    path('Hod/Student/View',Hod_views.VIEW_STUDENT,name= 'view_student'),
    path('Hod/Student/Edit/<str:id>',Hod_views.EDIT_STUDENT,name='edit_student'),
    path('Hod/Student/Delete/<str:admin>', Hod_views.DELETE_STUDENT,name='delete_student'),

    # Staff

    path('staff/add/', Hod_views.ADD_STAFF, name='add_staff'),
    path('staff/<int:id>/edit/', Hod_views.EDIT_STAFF, name='edit_staff'),
    path('staff/<int:id>/delete/', Hod_views.DELETE_STAFF, name='delete_staff'),
    path('staff/', Hod_views.VIEW_STAFF, name='view_staff'),

    path('Hod/Session/Add',Hod_views.ADD_SESSION,name= 'add_session'),
    path('Hod/Session/View,',Hod_views.VIEW_SESSION,name = 'view_session'),
    path('Hod/Session/Edit/<str:id>',Hod_views.EDIT_SESSION, name = 'edit_session'),
    path('Hod/Session/Update',Hod_views.UPDATE_SESSION,name='update_session'),
    path('Hod/Session/Delete/<str:id>' ,Hod_views.DELETE_SESSION,name = 'delete_session'),

    path('Hod/Staff/Send_Notification',Hod_views.STAFF_SEND_NOTIFICATION,name ='staff_send_notification'),
    path('Hod/Staff/save_notification',Hod_views.SAVE_NOTIFICATION,name='save_staff_notification'),

    path('Hod/Staff/Leave', Hod_views.STAFF_LEAVE_VIEW, name='staff_leave_view'),
    path("Hod/Staff/approve_leave/<str:id>",Hod_views.STAFF_APPROVE_LEAVE,name = 'staff_approve_leave'),
    path("Hod/Staff/disapprove_leave/<str:id>",Hod_views.STAFF_DISAPPROVE_LEAVE,name = 'staff_disapprove_leave'),

    path('Hod/staff/feedback',Hod_views.STAFF_FEEDBACK, name='staff_feedback' ),
    path('Hod/staff/feedback_reply',Hod_views.STAFF_FEEDBACK_REPLY, name='staff_feedback_reply' ),



    #this is a Staff url

    path('Staff/Home',Staff_Views.HOME,name = 'staff_home'),
    path('Staff/Notification',Staff_Views.NOTIFICATIONS,name = 'notification'),
    path('Staff/mark_as_done/<str:status',Staff_Views.STAFF_NOTIFICATION_MARK_AS_DONE,name='staff_notification_mark_as_done'),
    path('Staff/Apply_leave',Staff_Views.STAFF_APPLY_LEAVE,name= 'staff_apply_leave'),
    path('Staff/Apply_leave_save',Staff_Views.STAFF_APPLY_LEAVE_SAVE,name = 'staff_apply_leave_save'),
    path('staff/feedback',Staff_Views.STAFF_FEEDBACK,name='staff-feedback'),
    path('staff/feedback/save',Staff_Views.STAFF_FEEDBACK_SAVE,name='staff_feedback_save'),



    # question url
    path('question/', include('question.urls')),
    # 

    # course url

    path('course/', include('course.urls')),
    path('seatplan/', include('seatplan.urls')),

  
# Teacher subject select
    path('subject-choice/create/', TeacherSubjectChoiceCreateView.as_view(), name='subject_choice_create'),
    path('subject-choice/update/<int:pk>/', TeacherSubjectChoiceUpdateView.as_view(), name='subject_choice_update'),
    path('teacher/<int:pk>/pdf/', pdf_view, name='teacher_subject_choices_pdf'),
    path('ajax/load-semesters/', load_semesters, name='ajax_load_semesters'),
    path('ajax/load-subjects/', load_subjects, name='ajax_load_subjects'),
    path('ajax/get-total-credits/', ajax_get_total_credits, name='ajax_get_total_credits'),

    path('teacher-subject-choices/', teacher_subject_choice_list, name='teacher-subject-choice-list'),
    path('teacher/<int:pk>/subject/', TeacherSubjectChoiceListView.as_view(), name='teacher_Subject'),


    path('ajax/check_higher_rank_completion/', check_higher_rank_completion, name='check_higher_rank_completion'),






]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
