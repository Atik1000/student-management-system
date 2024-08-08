from django.urls import path
from .views import (BatchCreateView, BatchListView, GenerateSeatPlan, load_departments,
    load_semesters, RoomCreateView, RoomDetailView, RoomListView, RoomSeatPlanDetailView,
    RoomUpdateView, SeatPlanRoomCreateView, SeatPlanRoomDetailView)

urlpatterns = [
    # Room URLs
    path('room/', RoomListView.as_view(), name='room_list'),
    path('room/create/', RoomCreateView.as_view(), name='room_create'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room_update'),
    path('room/<int:pk>/detail/', RoomDetailView.as_view(), name='room_detail'),
    path('room/generate-seatplan/', GenerateSeatPlan.as_view(), name='generate_seat_plan'),
    path('batch/create/', BatchCreateView.as_view(), name='create_batch'),
    path('batch/list/', BatchListView.as_view(), name='batch_list'),
    path('ajax/load-departments/', load_departments, name='load_departments'),
    path('ajax/load-semesters/', load_semesters, name='load_semesters'),

    path('room/<int:pk>/create_seatplan/', SeatPlanRoomCreateView.as_view(), name='create_seatplan'),
    path('room/<int:pk>/seatplan/', SeatPlanRoomDetailView.as_view(), name='seatplan_detail'),

    path('room/<int:pk>/', RoomSeatPlanDetailView.as_view(), name='room_seatplan_detail'),


]