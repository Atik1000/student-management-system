

from django.contrib import admin
from  .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(Room)

admin.site.register(Batch)

admin.site.register(SeatPlan)




