# Generated by Django 4.0.2 on 2022-02-26 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='principal_fname',
        ),
        migrations.RemoveField(
            model_name='school',
            name='principal_lname',
        ),
        migrations.RemoveField(
            model_name='school',
            name='principal_phone',
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(help_text='+99801112233', max_length=15, unique=True)),
                ('work_place', models.CharField(choices=[('1-maktab', '1-maktab'), ('2-maktab', '2-maktab'), ('3-maktab', '3-maktab'), ('4-maktab', '4-maktab'), ('5-maktab', '5-maktab'), ('6-maktab', '6-maktab'), ('7-maktab', '7-maktab'), ('8-maktab', '8-maktab'), ('9-maktab', '9-maktab'), ('10-maktab', '10-maktab'), ('11-maktab', '11-maktab'), ('12-maktab', '12-maktab'), ('13-maktab', '13-maktab'), ('14-maktab', '14-maktab'), ('15-maktab', '15-maktab'), ('16-maktab', '16-maktab'), ('17-maktab', '17-maktab'), ('18-maktab', '18-maktab'), ('19-maktab', '19-maktab'), ('20-maktab', '22-maktab'), ('23-maktab', '23-maktab'), ('24-maktab', '24-maktab'), ('25-maktab', '25-maktab'), ('26-maktab', '26-maktab')], default='1-maktab', max_length=15, unique=True, verbose_name='Maktab nomi')),
                ('user_status', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
