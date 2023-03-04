# Generated by Django 4.1 on 2022-10-20 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'Admin'), (1, 'Teacher'), (2, 'Student')], default=2),
        ),
    ]
