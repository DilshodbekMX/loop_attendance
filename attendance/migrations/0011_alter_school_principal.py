# Generated by Django 4.0.2 on 2022-02-27 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0010_alter_teacher_work_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='principal',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_principal', to=settings.AUTH_USER_MODEL),
        ),
    ]
