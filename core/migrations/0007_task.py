# Generated by Django 4.1.2 on 2022-11-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('complete', models.BooleanField(default=False)),
                ('create', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['complete'],
            },
        ),
    ]
