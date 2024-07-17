from django.contrib import admin
from  .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('sub_code', 'sub_name', 'credit')
    search_fields = ('sub_code', 'sub_name')

class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(Program)

admin.site.register(Department)

admin.site.register(Semester)
admin.site.register(Course)

admin.site.register(Teacher)

# admin.site.register(Subject)

admin.site.register(Routine)







