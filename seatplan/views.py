from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView,DetailView
from django.urls import reverse_lazy
from app.models import Student
from course.models import Department, Program, Semester
from .models import Room, SeatPlan
from .forms import SeatPlanForm,RoomForm
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SeatPlanGenerateForm

# class RoomDetailView(DetailView):
#     model = Room
#     template_name = 'room/room_detail.html'
#     context_object_name = 'room'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Add programs for selection
#         programs = Program.objects.all()
#         context['programs'] = programs

#         # If program is selected, filter departments
#         program_id = self.request.GET.get('program')
#         if program_id:
#             departments = Department.objects.filter(program_id=program_id)
#             context['departments'] = departments

#         # If department is selected, filter semesters
#         department_id = self.request.GET.get('department')
#         if department_id:
#             semesters = Semester.objects.filter(department_id=department_id)
#             context['semesters'] = semesters

#         # Add form for generating seat plan
#         context['form'] = SeatPlanGenerateForm()

#         return context

class RoomDetailView(DetailView):
    model = Room
    template_name = 'room/room_detail.html'
    context_object_name = 'room'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        context['departments'] = Department.objects.all()
        context['semesters'] = Semester.objects.all()
        context['seat_plan_form'] = SeatPlanGenerateForm()
        context['seat_layout'] = self.get_seat_layout()
        return context
    
    def get_seat_layout(self):
        room = self.get_object()
        seat_plans = SeatPlan.objects.filter(room=room)
        layout = [['' for _ in range(room.num_columns)] for _ in range((room.num_seats // room.num_columns))]
        
        for seat_plan in seat_plans:
            row = (seat_plan.seat_number - 1) // room.num_columns
            col = (seat_plan.seat_number - 1) % room.num_columns
            layout[row][col] = seat_plan.student.admin.get_full_name()
        
        return layout


class GenerateSeatPlan(View):
    def post(self, request, *args, **kwargs):
        form = SeatPlanGenerateForm(request.POST)

        if form.is_valid():
            room_id = form.cleaned_data['room']
            semester_id = form.cleaned_data['semester']

            room = Room.objects.get(id=room_id)
            semester = Semester.objects.get(id=semester_id)

            # Generate seat plan logic - for example, create SeatPlan objects
            # You can adjust this according to your specific logic and requirements

            # Dummy logic to create seat plan
            students = Student.objects.filter(semester=semester)

            num_columns = room.num_columns
            seats_per_column = room.num_seats // num_columns

            seat_number = 1
            for student in students:
                for column in range(num_columns):
                    SeatPlan.objects.create(
                        room=room,
                        student=student,
                        seat_number=seat_number
                    )
                    seat_number += 1
                    if seat_number > room.num_seats:
                        break

            # Redirect to room detail view after generating seat plan
            return redirect('room_detail', pk=room_id)

        # If form is not valid, render room detail view with errors
        room_id = request.POST.get('room')
        return redirect('room_detail', pk=room_id)





    
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        seats_per_column = room.num_seats // room.num_columns
        seat_layout = [
            [f'{column + 1}-{row + 1}' for column in range(room.num_columns)]
            for row in range(seats_per_column)
        ]
        context['seat_layout'] = seat_layout
        return context

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