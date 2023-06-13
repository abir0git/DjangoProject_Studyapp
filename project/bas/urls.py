from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('create-room/', views.createroom, name="createRoom"),
    path('room/<str:pk>/update-room/', views.updateroom, name="updateRoom"),
    path('room/<str:pk>/delete-room/', views.deleteRoom, name="deleteRoom"),
]