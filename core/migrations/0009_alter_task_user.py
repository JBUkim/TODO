# Generated by Django 4.1.2 on 2022-11-19 07:16

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.CharField(max_length=100, verbose_name=django.contrib.auth.models.User),
        ),
    ]
