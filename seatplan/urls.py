from django.urls import path
from .views import (
    RoomListView, RoomCreateView, RoomUpdateView,RoomDetailView,
    SeatPlanListView, SeatPlanCreateView
)

urlpatterns = [
    # Room URLs
    path('room/', RoomListView.as_view(), name='room_list'),
    path('room/create/', RoomCreateView.as_view(), name='room_create'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room_update'),

    path('room/<int:pk>/detail/', RoomDetailView.as_view(), name='room_detail'),


    # SeatPlan URLs
    path('seatplan/', SeatPlanListView.as_view(), name='seatplan_list'),
    path('seatplan/create/', SeatPlanCreateView.as_view(), name='seatplan_create'),
]