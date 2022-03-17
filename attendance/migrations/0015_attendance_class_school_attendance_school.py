# Generated by Django 4.0.2 on 2022-03-02 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0014_remove_attendance_class_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='class_school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.schoolclass'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.school'),
            preserve_default=False,
        ),
    ]
