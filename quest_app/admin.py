from django.contrib import admin
from .models import Habit, Quest

# モデルを管理画面に登録
admin.site.register(Habit)
admin.site.register(Quest)
