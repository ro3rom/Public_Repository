# Generated by Django 5.1.3 on 2024-12-13 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest_app', '0007_rename_total_points_userprofile_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitQuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('points_required', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='questcompletion',
            name='quest',
        ),
        migrations.RemoveField(
            model_name='questcompletion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='habit',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='habit',
            name='quest',
        ),
        migrations.RemoveField(
            model_name='habit',
            name='user',
        ),
        migrations.RemoveField(
            model_name='point',
            name='points',
        ),
        migrations.RemoveField(
            model_name='point',
            name='user',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='completed_at',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='start_date',
        ),
        migrations.AddField(
            model_name='point',
            name='description',
            field=models.CharField(default='Default description', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='point',
            name='value',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reward',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='habit',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='quest',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='quest',
            name='points',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='quest',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='QuestCompletion',
        ),
    ]
