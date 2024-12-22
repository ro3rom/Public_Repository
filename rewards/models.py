from django.db import models

# Create your models here.
from django.db import models

class Reward(models.Model):
    title = models.CharField(max_length=100)  # 報酬名
    description = models.TextField()          # 詳細
    cost = models.PositiveIntegerField()      # 必要ポイント

    def __str__(self):
        return self.title
