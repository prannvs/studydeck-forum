from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
]