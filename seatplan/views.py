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
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Count, Q, F
from django.http import HttpResponse
from django.template.loader import get_template


class RoomListView(ListView):
    model = Room
    template_name = 'room/room_list.html'
    context_object_name = 'rooms'


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'room/room_form.html'
    success_url = reverse_lazy('room_list')


class RoomUpdateView(UpdateView):
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

        # Fetch all seat plans related to the room, ordered by seat number
        seat_plans = SeatPlan.objects.filter(room=room).select_related('student').order_by('seat_number')

        # Group students by their semester (batch)
        students_by_batch = {}
        for seat_plan in seat_plans:
            if seat_plan.student:
                batch_name = seat_plan.student.semester.name  # Using semester name as the batch name
                if batch_name not in students_by_batch:
                    students_by_batch[batch_name] = []
                students_by_batch[batch_name].append(seat_plan.student.roll_no)

        # Ensure we have two types of batches (assuming only two semesters)
        batch_names = list(students_by_batch.keys())
        if len(batch_names) < 2:
            # Handle case where less than two semesters are present
            batch_names.append('Empty')

        # Determine the number of columns and rows
        num_columns = room.num_columns
        num_seats_per_column = room.num_seats // num_columns

        # Initialize seat layout
        seat_layout = [[None for _ in range(num_columns)] for _ in range(num_seats_per_column)]

        # Prepare to fill columns alternatively
        students_batch_1 = students_by_batch.get(batch_names[0], [])
        students_batch_2 = students_by_batch.get(batch_names[1], [])

        # Fill columns alternately with students
        for col_index in range(num_columns):
            if col_index % 2 == 0:
                # Even index columns - fill with students from the first batch
                current_students = students_batch_1
            else:
                # Odd index columns - fill with students from the second batch
                current_students = students_batch_2

            # Fill each row in the current column
            for row_index in range(num_seats_per_column):
                if current_students:
                    seat_layout[row_index][col_index] = current_students.pop(0)  # Remove the student after assigning
                else:
                    seat_layout[row_index][col_index] = 'Empty'  # Mark empty if no students left

        # Update the context
        context['seat_layout'] = seat_layout
        context['batches'] = batch_names  # List of batch names for the table header
        return context

class SeatPlanGenerateView(View):
    template_name = 'room/seatplan_form.html'

    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['pk'])
        # Only select semesters with students that still need to be seated
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

        # Retrieve unseated students from the selected semesters
        students_by_semester = {
            semester: list(semester.students.filter(seatplan__isnull=True).order_by('roll_no')) for semester in semesters
        }

        num_columns = room.num_columns
        num_rows = room.num_seats // num_columns

        # Initialize seating logic
        seat_plan_data = []
        semester_a, semester_b = semesters[0], semesters[1]
        semester_a_students = students_by_semester[semester_a]
        semester_b_students = students_by_semester[semester_b]

        # Fill seats for Semester A in odd columns (1, 3, etc.)
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

        # Fill seats for Semester B in even columns (2, 4, etc.)
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

        # Check if there are remaining students to be seated
        if semester_a_students or semester_b_students:
            # Get the next available room (implement your own logic to find the next room)
            next_room = self.get_next_room(room)

            if next_room:
                return redirect('generate_seatplan', pk=next_room.pk)
            else:
                # No more rooms available, display a message
                return render(request, self.template_name, {
                    'room': room,
                    'semesters': semesters,
                    'error': "Not enough rooms available to seat all students."
                })

        return redirect('room_list')

    def get_next_room(self, current_room):
        """
        Function to get the next available room after the current room.
        You can customize this method to determine the logic for selecting the next room.
        For example, you might want to select the next room based on the room number or other criteria.
        """
        try:
            # Fetch the next room based on the room number or some other ordering criteria
            return Room.objects.filter(id__gt=current_room.id).order_by('id').first()
        except Room.DoesNotExist:
            return None



class RoomDetailPDFView(DetailView):
    model = Room  # Replace with your actual model
    template_name = 'room/room_detail.html'  # Adjust to your template path

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Make sure the object is set
        context = self.get_context_data(**kwargs)

        # Load the template
        template = get_template(self.template_name)
        html_string = template.render(context)

        # Convert the HTML to a PDF
        html = HTML(string=html_string)
        pdf_content = html.write_pdf()

        # Return the PDF response
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="room_{self.object.id}_details.pdf"'
        return response

