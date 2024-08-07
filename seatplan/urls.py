from django.urls import path
from .views import (GenerateSeatPlan, RoomCreateView, RoomDetailView, RoomListView, RoomUpdateView,
    SeatPlanCreateView, SeatPlanListView)

urlpatterns = [
    # Room URLs
    path('room/', RoomListView.as_view(), name='room_list'),
    path('room/create/', RoomCreateView.as_view(), name='room_create'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room_update'),

    path('room/<int:pk>/detail/', RoomDetailView.as_view(), name='room_detail'),


    # SeatPlan URLs
    path('seatplan/', SeatPlanListView.as_view(), name='seatplan_list'),
    path('seatplan/create/', SeatPlanCreateView.as_view(), name='seatplan_create'),
    path('room/<int:pk>/generate-seatplan/', GenerateSeatPlan.as_view(), name='generate_seat_plan'),

]