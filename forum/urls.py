from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('thread/<slug:slug>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('thread/<slug:slug>/lock/', views.lock_thread, name='lock_thread'),
    path('thread/<slug:slug>/delete/', views.delete_thread, name='delete_thread'),
]