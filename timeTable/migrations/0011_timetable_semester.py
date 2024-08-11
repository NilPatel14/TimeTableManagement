# Generated by Django 4.1.7 on 2024-08-11 12:40

from django.db import migrations, models
import django.db.models.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('timeTable', '0010_timetable_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.fields.related.ForeignKey, to='timeTable.semester'),
        ),
    ]
