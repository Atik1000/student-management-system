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
        num_columns = room.num_columns
        num_seats_per_column = room.num_seats // num_columns

        # Retrieve students by semester
        semesters = Semester.objects.all().order_by('name')
        students_by_semester = {semester.name: list(Student.objects.filter(semester=semester).order_by('roll_no')) for semester in semesters}

        seat_layout = [[] for _ in range(num_seats_per_column)]
        current_column = 0

        # Iterate over students and fill the seat layout
        for semester_name, students in students_by_semester.items():
            student_index = 0

            while student_index < len(students):
                for row in seat_layout:
                    if current_column < num_columns:
                        if student_index < len(students):
                            row.append((f'{current_column + 1}-{len(row) + 1}', students[student_index]))
                            student_index += 1
                        else:
                            row.append((f'{current_column + 1}-{len(row) + 1}', None))
                    else:
                        break
                current_column += 1

        context['seat_layout'] = seat_layout
        context['semester_headers'] = semesters
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
        semesters = request.POST.getlist('semesters')
        students = Student.objects.filter(semester__in=semesters).order_by('roll_no')
        
        seats_per_column = room.num_seats // room.num_columns
        seat_layout = [
            [f'{column + 1}-{row + 1}' for column in range(room.num_columns)]
            for row in range(seats_per_column)
        ]
        
        index = 0
        for row in seat_layout:
            for seat in row:
                if index < len(students):
                    SeatPlan.objects.create(
                        room=room,
                        semester=students[index].semester,
                        student=students[index],
                        seat_number=seat
                    )
                    index += 1

        return redirect('room_detail', pk=room.pk)
