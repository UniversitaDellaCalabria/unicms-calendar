# Generated by Django 3.2.5 on 2022-02-11 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicms_calendar', '0006_alter_calendar_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]