# Generated by Django 4.0.2 on 2022-03-15 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0032_alter_student_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='total',
        ),
        migrations.AlterField(
            model_name='student',
            name='absent',
            field=models.IntegerField(blank=True, verbose_name="Yo'q"),
        ),
        migrations.AlterField(
            model_name='student',
            name='cause',
            field=models.IntegerField(blank=True, verbose_name='Sababli'),
        ),
        migrations.AlterField(
            model_name='student',
            name='present',
            field=models.IntegerField(blank=True, null=True, verbose_name='Bor'),
        ),
    ]
