# Generated by Django 4.0.2 on 2022-02-27 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_alter_school_principal_alter_school_school_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='work_place',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacherschool', to='attendance.school'),
        ),
    ]