# Generated by Django 4.0.4 on 2022-05-21 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_remove_doctor_name_doctor_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='image',
            field=models.ImageField(default='doctor_avatar.svg', upload_to='doctor_profile_pics'),
        ),
    ]