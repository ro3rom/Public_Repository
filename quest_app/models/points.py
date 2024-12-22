# quest_app/models/points.py

from django.db import models

class Point(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.description} ({self.value} ポイント)"
