# Generated by Django 4.0.4 on 2022-05-25 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_remove_medicine_producer_medicine_producer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='medicine',
            field=models.ManyToManyField(to='pets.medicine'),
        ),
    ]
