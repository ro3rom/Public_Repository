# quest_app/models/reward.py

from django.db import models
from django.contrib.auth.models import User


class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # descriptionは任意
    points_required = models.PositiveIntegerField()  # points_requiredを定義
    
    def __str__(self):
        return self.name
