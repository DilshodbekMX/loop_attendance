# Generated by Django 4.0.2 on 2022-03-11 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0030_student_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]