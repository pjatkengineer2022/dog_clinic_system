# Generated by Django 4.0.4 on 2022-05-28 09:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0006_remove_treatment_medicine_medicinehistory_medicine_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicinehistory',
            name='expectedEnd',
        ),
        migrations.AlterField(
            model_name='medicine',
            name='producer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pets.producer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicinehistory',
            name='startDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='start',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]