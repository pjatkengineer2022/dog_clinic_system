# Generated by Django 4.0.4 on 2022-05-28 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_service_alter_doctorshift_doctor_doctor_service'),
        ('visits', '0003_alter_status_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='service',
        ),
        migrations.AlterField(
            model_name='visit',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visits', to='doctors.doctor'),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]