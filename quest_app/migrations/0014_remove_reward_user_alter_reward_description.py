# Generated by Django 5.1.3 on 2024-12-16 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest_app', '0013_reward_description_reward_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='user',
        ),
        migrations.AlterField(
            model_name='reward',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
