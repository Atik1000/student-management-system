from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView,DetailView
from django.urls import reverse_lazy
from app.models import Student
from course.models import Department, Program, Semester
from .models import Batch, Room, SeatPlan, SeatPlanRoom
from .forms import BatchForm, RoomForm, SeatPlanForm
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SeatPlanGenerateForm
# views.py
from django.http import JsonResponse
from .forms import SeatPlanRoomForm

class SeatPlanRoomCreateView(CreateView):
    model = SeatPlanRoom
    form_class = SeatPlanRoomForm
    template_name = 'room/seatplanroom_form.html'
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        room_pk = self.kwargs['pk']
        room = get_object_or_404(Room, pk=room_pk)
        form.instance.room = room
        return super().form_valid(form)

class SeatPlanRoomDetailView(DetailView):
    model = Room
    template_name = 'room/seatplanroom_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        context['seatplanrooms'] = SeatPlanRoom.objects.filter(room=room)
        return context
    




def load_departments(request):
    program_id = request.GET.get('program')
    departments = Department.objects.filter(program_id=program_id).order_by('name')
    return JsonResponse(list(departments.values('id', 'name')), safe=False)

def load_semesters(request):
    department_id = request.GET.get('department')
    semesters = Semester.objects.filter(department_id=department_id).order_by('name')
    return JsonResponse(list(semesters.values('id', 'name')), safe=False)


    
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
        print(Department.objects.all())  
        context['seat_layout'] = seat_layout
        return context

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room/room_form.html'
    success_url = reverse_lazy('room_list')

class GenerateSeatPlan(View):
    template_name = 'room/seatplan.html'

    def get(self, request):
        form = SeatPlanGenerateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SeatPlanGenerateForm(request.POST)

        if form.is_valid():
            room_id = form.cleaned_data['room'].id
            semester_id = form.cleaned_data['semester'].id

            room = Room.objects.get(id=room_id)
            semester = Semester.objects.get(id=semester_id)

            # Generate seat plan logic
            students = Student.objects.filter(semester=semester)

            num_columns = room.num_columns
            seats_per_column = room.num_seats // num_columns

            SeatPlan.objects.filter(room=room).delete()  # Clear existing seat plans for the room

            seat_number = 1
            for student in students:
                for column in range(num_columns):
                    if seat_number <= room.num_seats:
                        SeatPlan.objects.create(
                            room=room,
                            student=student,
                            seat_number=seat_number
                        )
                        seat_number += 1

            return redirect('room_detail', pk=room_id)

        return render(request, self.template_name, {'form': form})




class BatchCreateView(CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'batch/batch_form.html'
    success_url = reverse_lazy('batch_list')  # Redirect to batch list view upon successful form submission

class BatchListView(ListView):
    model = Batch
    template_name = 'batch/batch_list.html'
    context_object_name = 'batches'  # Name of the context variable for batches list


# combination view 

class RoomSeatPlanDetailView(DetailView):
    model = Room
    template_name = 'room/room_seatplan_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()

        # Seat layout logic
        seats_per_column = room.num_seats // room.num_columns
        seat_layout = [
            [f'{column + 1}-{row + 1}' for column in range(room.num_columns)]
            for row in range(seats_per_column)
        ]

        # Seat plan rooms
        seatplanrooms = SeatPlanRoom.objects.filter(room=room)

        # Add to context
        context['seat_layout'] = seat_layout
        context['seatplanrooms'] = seatplanrooms
        return context