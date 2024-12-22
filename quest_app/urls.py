from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

app_name = 'quest_app'  # 名前空間を設定

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('habit_list/', views.habit_list, name='habit_list'),
    path('add_habit/', views.add_habit, name='add_habit'),
    path('add_quest/', views.add_quest, name='add_quest'),
    path('edit_quest/<int:quest_id>/', views.edit_quest, name='edit_quest'),
    path('delete_quest/<int:quest_id>/', views.delete_quest, name='delete_quest'),
    path('exchange_points/', views.exchange_points, name='exchange_points'),
    path('quest_list/', views.quest_list, name='quest_list'),
    path('complete_quest/<int:quest_id>/', views.complete_quest, name='complete_quest'),
    path('add_reward/', views.add_reward, name='add_reward'),
    path('rewards/<int:reward_id>/edit/', views.edit_reward, name='edit_reward'),
    path('edit_user/', views.edit_user, name='edit_user'),  
    path('reward_list/', views.reward_list, name='reward_list'),
    path('reward_delete/<int:reward_id>/', views.reward_delete, name='reward_delete'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ]
