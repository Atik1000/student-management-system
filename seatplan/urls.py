from django.urls import path
from .views import (RoomCreateView, RoomDetailView, RoomListView,
                    RoomUpdateView,SeatPlanGenerateView,RoomDetailPDFView)

urlpatterns = [
    # Room URLs
    path('room/', RoomListView.as_view(), name='room_list'),
    path('room/create/', RoomCreateView.as_view(), name='room_create'),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name='room_update'),
    path('room/<int:pk>/detail/', RoomDetailView.as_view(), name='room_detail'),
    path('room/<int:pk>/generate-seatplan/', SeatPlanGenerateView.as_view(), name='generate_seatplan'),
    path('room/<int:pk>/pdf/', RoomDetailPDFView.as_view(), name='room_detail_pdf'),



]