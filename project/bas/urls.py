from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="Login"),
    path('logout/', views.logoutUser, name="Logout"),
    path('register/', views.registerUser, name="Register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="Room"),
    path('profile/<str:pk>/', views.userProfile, name="userProfile"),
    path('create-room/', views.createroom, name="createRoom"),
    path('room/<str:pk>/update-room/', views.updateroom, name="updateRoom"),
    path('room/<str:pk>/delete-room/', views.deleteRoom, name="deleteRoom"),
]