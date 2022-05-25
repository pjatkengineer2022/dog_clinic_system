# Generated by Django 4.0.4 on 2022-05-25 18:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pets', '0004_alter_treatment_medicine'),
        ('doctors', '0004_shift_alter_doctor_image_doctorshift'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('odbyta', 'odbyta'), ('nieodbyta', 'nieodbyta')], default='nieodbyta', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ownerComment', models.CharField(blank=True, max_length=2000, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctors.doctor')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet')),
                ('service', models.ManyToManyField(to='visits.service')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.status')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
                ('treatment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pets.treatment')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.visit')),
            ],
        ),
    ]
