from django.shortcuts import render,redirect
from app.models import Staff, Staff_Feedback, Staff_leave, Staff_Notification
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
    staff = Staff.objects.filter(admin=request.user.id)

    # Initialize context with a default value
    context = {
        'staff_leave_history': None,
    }

    if staff.exists():
        staff_id = staff.first().id  # Get the ID of the first staff (assuming one-to-one relationship with user)
        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)
        context['staff_leave_history'] = staff_leave_history

    return render(request, 'Staff/apply_leave.html', context)


def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        
        if not leave_date or not leave_message:
            messages.warning(request, "Please fill out all fields.")
            return redirect('staff_apply_leave')

        try:
            staff = Staff.objects.get(admin=request.user.id)
            leave = Staff_leave(
                staff_id=staff,
                date=leave_date,
                message=leave_message,
            )
            leave.save()
            messages.success(request, "Staff leave successfully sent.")
            return redirect('staff_apply_leave')
        except Staff.DoesNotExist:
            messages.error(request, "Staff not found.")
            return redirect('staff_apply_leave')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('staff_apply_leave')
    else:
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
    
