# quest_app/models/quest.py

from django.db import models

class Quest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    def is_completed(self):
        return self.completed_at is not None
