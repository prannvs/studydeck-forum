from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('thread/<slug:slug>/', views.thread_detail, name='thread_detail'),
    path('create/', views.create_thread, name='create_thread'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('thread/<slug:slug>/lock/', views.lock_thread, name='lock_thread'),
    path('thread/<slug:slug>/delete/', views.delete_thread, name='delete_thread'),
    path('reply/<int:reply_id>/like/', views.like_reply, name='like_reply'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
    path('thread/<slug:slug>/like/', views.like_thread, name='like_thread'),
    path('thread/<slug:slug>/report/', views.report_thread, name='report_thread'),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('moderator/resolve/<slug:slug>/', views.resolve_report, name='resolve_report'),
]