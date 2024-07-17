from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView,DetailView
from django.urls import reverse_lazy
from app.models import Student
from .models import Room, SeatPlan
from .forms import SeatPlanForm,RoomForm

    
class SeatPlanListView(ListView):
    model = SeatPlan
    template_name = 'room/seatplan_list.html'
    context_object_name = 'seatplans'

class SeatPlanCreateView(CreateView):
    model = SeatPlan
    form_class = SeatPlanForm
    template_name = 'room/seatplan_form.html'
    success_url = reverse_lazy('seatplan_list')


class RoomListView(ListView):
    model = Room
    template_name = 'room/room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'room/room_form.html'
    success_url = reverse_lazy('room_list')


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room/room_detail.html'
    context_object_name = 'room'

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room/room_form.html'
    success_url = reverse_lazy('room_list')

def generate_seat_plan(request, room_number):
    room = get_object_or_404(Room, number=room_number)
    students = Student.objects.all()
    for student in students:
        try: 
            SeatPlan.objects.get(student=student)
        except SeatPlan.DoesNotExist:
            total_seat = SeatPlan.objects.filter(room=room).count()
            if room.num_seats < total_seat + 1:
                SeatPlan.objects.create(room=room, student=student, seat_number=total_seat + 1)

    context = {
        'room': room,
    }
    return render(request, 'seat_plan.html', context)