# shukanka_quest/urls.py
from django.contrib import admin
from django.urls import path, include
from users import views as user_views  # users/views.py のビューをインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),  # トップページ（/）のパスを追加
    path('register/', user_views.register, name='register'),  # 登録ページ
]
