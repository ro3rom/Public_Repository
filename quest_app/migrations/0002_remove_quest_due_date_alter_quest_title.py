# Generated by Django 5.1.3 on 2024-12-11 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quest',
            name='due_date',
        ),
        migrations.AlterField(
            model_name='quest',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
