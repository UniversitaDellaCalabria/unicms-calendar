# Generated by Django 3.2.5 on 2021-12-13 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unicms_calendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='tags',
        ),
    ]
