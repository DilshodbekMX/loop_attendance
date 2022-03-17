# Generated by Django 4.0.2 on 2022-03-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0026_student_cause_alter_student_absent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='middle_name',
        ),
        migrations.AddField(
            model_name='student',
            name='student_name',
            field=models.CharField(default=1, max_length=100, verbose_name="O'quvchi FISH"),
            preserve_default=False,
        ),
    ]
