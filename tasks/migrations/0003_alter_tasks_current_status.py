# Generated by Django 4.2.7 on 2024-01-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_tasks_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='current_status',
            field=models.CharField(choices=[('to-do(incomplete)', 'to-do(incomplete)'), ('on-going', 'on-going'), ('completed', 'completed')], max_length=100),
        ),
    ]