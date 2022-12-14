# Generated by Django 4.1.3 on 2022-11-02 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(blank=True, max_length=100, null=True)),
                ('medication_dose', models.CharField(blank=True, max_length=100, null=True)),
                ('medication_frequency', models.CharField(blank=True, max_length=100, null=True)),
                ('medication_details', models.CharField(max_length=100)),
                ('status', models.CharField(default='inactive', max_length=100)),
                ('patient_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patientregister')),
            ],
            options={
                'db_table': 'medications',
            },
        ),
        migrations.CreateModel(
            name='PainSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('answer_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.painanswers')),
                ('patient_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patientregister')),
                ('question_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.painquestions')),
            ],
            options={
                'db_table': 'pain_selection',
            },
        ),
        migrations.RemoveField(
            model_name='paintypetable',
            name='patient_fk',
        ),
        migrations.AddField(
            model_name='paindetails',
            name='acupuncture',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='alcohol',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='alcohol_day',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='awake_pain',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='blood_hospital',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='blood_professional',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='blood_tests',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='chiropractor',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='collars',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='decrease_pain_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='increase_pain_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='injections',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='major_illness_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='medication_sleep',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='mental_support',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='mentalservices',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='nerve_hospital',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='nerve_professional',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='nerve_tests',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='no_pain',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='often_pain',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='other_llness_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='other_treatments',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='pain_free',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='physical_activity_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='physiotherapy',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='present_pain_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='psychology',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='relieve_pain_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='scan_hospital',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='scan_professional',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='scans',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='smoke',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='smoke_day',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='spend_day_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='tens',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='time_of_pain_best',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='time_of_pain_worst',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='treatment_details_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='trouble_sleep',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='wheel_chair',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='x_rays',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='x_rays_hospital',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='paindetails',
            name='x_rays_professional',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paindetails',
            name='comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='paindetails',
            name='onset_of_pain',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paindetails',
            name='year_pain_began',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='PainStartTable',
        ),
        migrations.DeleteModel(
            name='PainTypeTable',
        ),
    ]
