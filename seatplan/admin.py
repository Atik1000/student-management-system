

from django.contrib import admin
from  .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(Room)


# admin.site.register(SeatPlan)

@admin.register(SeatPlan)
class SeatPlanAdmin(admin.ModelAdmin):
    list_display=['id','room','semester','student','col_num','seat_number']



