# Generated by Django 4.0.5 on 2022-11-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_medications_other_medication'),
    ]

    operations = [
        migrations.AddField(
            model_name='paindetails',
            name='mood_changed',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='ways_relax',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]