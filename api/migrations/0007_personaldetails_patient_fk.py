# Generated by Django 4.1.3 on 2022-11-09 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_personaldetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='patient_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.patientregister'),
            preserve_default=False,
        ),
    ]
