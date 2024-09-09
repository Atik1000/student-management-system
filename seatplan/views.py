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
from django.db import models

from django.db.models import Count, Q, F

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

        # Fetch all seat plans for this room
        seat_plans = SeatPlan.objects.filter(room=room).select_related('student').order_by('seat_number')

        # Prepare seat layout based on the room configuration
        num_columns = room.num_columns
        num_seats_per_column = room.num_seats // num_columns
        seat_layout = [[] for _ in range(num_seats_per_column)]

        # Iterate over seat plans and populate the seat layout
        for seat_plan in seat_plans:
            seat_number = int(seat_plan.seat_number)  # Ensure seat_number is an integer
            column_index = (seat_number - 1) % num_columns
            row_index = (seat_number - 1) // num_columns

            # Adjust the seat layout to place the student in the correct position
            while len(seat_layout[row_index]) <= column_index:
                seat_layout[row_index].append(None)
            seat_layout[row_index][column_index] = seat_plan

        context['seat_layout'] = seat_layout
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
        semesters = Semester.objects.annotate(
            student_count=Count('students'),
            seated_students_count=Count('students', filter=Q(students__seatplan__isnull=False))
        ).filter(student_count__gt=models.F('seated_students_count')).order_by('name')

        return render(request, self.template_name, {'room': room, 'semesters': semesters})

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['pk'])
        selected_semesters = request.POST.getlist('semesters')
        semesters = Semester.objects.filter(pk__in=selected_semesters).order_by('name')

        if len(semesters) != 2:
            return render(request, self.template_name, {'room': room, 'semesters': semesters, 'error': "Please select exactly two semesters."})

        students_by_semester = {
            semester: list(semester.students.order_by('roll_no')) for semester in semesters
        }

        num_columns = room.num_columns
        num_rows = room.num_seats // num_columns

        # Initialize seating logic
        seat_plan_data = []
        semester_a, semester_b = semesters[0], semesters[1]
        semester_a_students = students_by_semester[semester_a]
        semester_b_students = students_by_semester[semester_b]

        # Filling seats for Semester A in odd columns (1, 3, etc.)
        for col_num in range(1, num_columns + 1, 2):  # Iterate over odd columns
            for row_num in range(1, num_rows + 1):
                if not semester_a_students:
                    break  # Break if no more students to seat
                student = semester_a_students.pop(0)
                seat_plan_data.append(SeatPlan(
                    room=room,
                    semester=semester_a,
                    student=student,
                    col_num=col_num,
                    seat_number=row_num
                ))

        # Filling seats for Semester B in even columns (2, 4, etc.)
        for col_num in range(2, num_columns + 1, 2):  # Iterate over even columns
            for row_num in range(1, num_rows + 1):
                if not semester_b_students:
                    break  # Break if no more students to seat
                student = semester_b_students.pop(0)
                seat_plan_data.append(SeatPlan(
                    room=room,
                    semester=semester_b,
                    student=student,
                    col_num=col_num,
                    seat_number=row_num
                ))

        # Bulk create the seat plans to optimize database performance
        SeatPlan.objects.bulk_create(seat_plan_data)

        return redirect('room_list')
