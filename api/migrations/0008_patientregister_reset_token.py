# Generated by Django 4.1.3 on 2022-11-10 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_personaldetails_patient_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientregister',
            name='reset_token',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
