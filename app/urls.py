from django.urls import path
from .views import RoutineCreateView, RoutineUpdateView

urlpatterns = [
    path('routine/add/', RoutineCreateView.as_view(), name='routine-add'),
  
    path('routine/<int:pk>/update/', RoutineUpdateView.as_view(), name='routine-update'),
  

]