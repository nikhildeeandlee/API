# Generated by Django 4.1.3 on 2022-11-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_patientregister_reset_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientregister',
            name='reset_token',
            field=models.CharField(default='', max_length=255),
        ),
    ]
