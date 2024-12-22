# quest_app/models/profile.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .reward import Reward  # もしRewardモデルが別のファイルにある場合

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)    
    points = models.PositiveIntegerField(default=0)  # PositiveIntegerFieldに変更
    other_field = models.CharField(max_length=100, blank=True)
    rewards = models.ManyToManyField(Reward, blank=True)  # ここで報酬を追加

    def __str__(self):
        return f'{self.user.username} Profile'

# シグナル：ユーザーが作成された時にProfileを作成
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()
