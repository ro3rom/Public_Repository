"""
URL configuration for shukanka_quest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from quest_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLoginView

urlpatterns = [
    path('', views.index, name='index'),  # ホームページ (仮トップ)
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),  # ホーム画面
    path('habit_list/', views.habit_list, name='habit_list'),  # 習慣リスト
    path('add_habit/', views.add_habit, name='add_habit'),  # 習慣追加
    path('quest_list/', views.quest_list, name='quest_list'),  # クエスト一覧
    path('exchange_points/', views.exchange_points, name='exchange_points'),  # ポイント交換
    path('initialize_points/', views.initialize_points, name='initialize_points'),  # ポイント初期化
    path('welcome/', views.welcome, name='welcome'),  # Welcome画面
    path('admin/', admin.site.urls),  # admin画面
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ログアウトURL
    path('edit_user/', views.edit_user, name='edit_user'),
    path('login/', views.login_view, name='login'),  # CustomLoginView を使用
    path('quest_app/', include('quest_app.urls')),  # quest_app の URL を含める
    path('delete_account/', views.delete_account, name='delete_account'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
