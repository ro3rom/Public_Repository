# Generated by Django 5.1.3 on 2024-12-12 06:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest_app', '0004_alter_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='quest',
            name='points',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='quest',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='QuestCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_completed', models.DateTimeField(auto_now_add=True)),
                ('points_earned', models.IntegerField()),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quest_app.quest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
