# Generated by Django 4.0.4 on 2022-05-26 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_alter_treatment_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(auto_now_add=True)),
                ('expectedEnd', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
