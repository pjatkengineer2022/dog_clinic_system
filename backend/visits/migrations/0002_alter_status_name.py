# Generated by Django 4.0.4 on 2022-05-26 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(choices=[('odbyta', 'odbyta'), ('nieodbyta', 'nieodbyta')], default='nieodbyta', max_length=100, unique=True),
        ),
    ]
