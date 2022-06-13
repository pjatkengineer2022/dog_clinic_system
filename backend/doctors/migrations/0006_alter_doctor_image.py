# Generated by Django 4.0.4 on 2022-05-30 08:53

import aaConfig.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_service_alter_doctorshift_doctor_doctor_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(default='doctor_avatar.png', upload_to='doctor_profile_pics', validators=[aaConfig.validators.validate_file_size]),
        ),
    ]
