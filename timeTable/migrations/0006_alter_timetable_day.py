# Generated by Django 4.1.7 on 2024-08-06 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeTable', '0005_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeTable.day'),
        ),
    ]
