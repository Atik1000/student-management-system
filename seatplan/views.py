from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView,DetailView
from django.urls import reverse_lazy
from app.models import Student
from course.models import Department, Program, Semester
from .models import Room, SeatPlan
from .forms import  RoomForm
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# views.py
from django.http import JsonResponse


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
        seat_plans = SeatPlan.objects.filter(room=room).order_by('seat_number')

        if seat_plans.exists():
            # Generate seat layout based on existing seat plans
            num_columns = room.num_columns
            num_seats_per_column = room.num_seats // num_columns
            seat_layout = [[] for _ in range(num_seats_per_column)]

            for seat_plan in seat_plans:
                seat_number = seat_plan.seat_number.split('-')
                column = int(seat_number[0]) - 1
                row = int(seat_number[1]) - 1
                seat_layout[row].append((seat_plan.seat_number, seat_plan.student))

            context['seat_layout'] = seat_layout
            context['semester_headers'] = seat_plans.values('semester__name').distinct()
        else:
            # Show basic seat layout
            num_columns = room.num_columns
            num_seats_per_column = room.num_seats // num_columns
            seat_layout = [
                [f'{col + 1}-{row + 1}' for col in range(num_columns)]
                for row in range(num_seats_per_column)
            ]
            context['seat_layout'] = seat_layout
            context['semester_headers'] = None

        return context



class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room/room_form.html'
    success_url = reverse_lazy('room_list')


class SeatPlanGenerateView(View):
    template_name = 'room/seatplan_form.html'
    
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['pk'])
        semesters = Semester.objects.all()
        return render(request, self.template_name, {'room': room, 'semesters': semesters})
    
    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['pk'])
        selected_semesters = request.POST.getlist('semesters')
        semesters = Semester.objects.filter(pk__in=selected_semesters).order_by('name')
        
        seats_per_column = room.num_seats // room.num_columns
        seat_layout = [[] for _ in range(seats_per_column)]

        # Organize students by semester
        students_by_semester = [list(Student.objects.filter(semester=semester).order_by('roll_no')) for semester in semesters]

        # Assign students to columns in a cyclic manner
        column_index = 0
        while any(students_by_semester):
            for row in seat_layout:
                if column_index < room.num_columns:
                    semester_index = column_index % len(semesters)
                    if students_by_semester[semester_index]:
                        student = students_by_semester[semester_index].pop(0)
                        seat_number = f'{column_index + 1}-{len(row) + 1}'
                        SeatPlan.objects.create(
                            room=room,
                            semester=semesters[semester_index],
                            student=student,
                            seat_number=seat_number
                        )
                        row.append((seat_number, student))
                    else:
                        row.append((f'{column_index + 1}-{len(row) + 1}', None))
                column_index += 1

        return redirect('room_detail', pk=room.pk)
