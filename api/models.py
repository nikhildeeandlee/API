from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.


# Patient Register
class PatientRegister(models.Model):
    patient_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)

    hospital_number = models.CharField(max_length=20, default="", blank=True)
    dateofbirth = models.CharField(max_length=10, default="")
    address = models.TextField(default="", blank=True)
    postcode = models.CharField(max_length=10, default="")

    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=255)
    reset_token = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "patient_reg"


# Doctor Register
class DoctorRegister(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    specialization = models.CharField(max_length=150)
    hospital_id = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)

    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=255)
    reset_token = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "doctor_reg"


# Tech Support Register
class TechRegister(models.Model):
    tech_id = models.AutoField(primary_key=True)
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    doctor_fk = models.ForeignKey(DoctorRegister, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.BigIntegerField()
    address = models.TextField()
    password1 = models.CharField(max_length=10)
    password2 = models.CharField(max_length=10)

    class Meta:
        db_table = "tech_reg"


# Pain Questions
class PainQuestions(models.Model):

    questions = models.CharField(max_length=255)

    class Meta:
        db_table = "pain_questions"


# Pain Answers
class PainAnswers(models.Model):

    answers = models.CharField(max_length=255)

    class Meta:
        db_table = "pain_answers"


# Pain Selection
class PainSelection(models.Model):
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    question_fk = models.ForeignKey(PainQuestions, on_delete=models.CASCADE)
    answer_fk = models.ForeignKey(PainAnswers, on_delete=models.CASCADE)
    key = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "pain_selection"


# Pain Details
class PainDetails(models.Model):
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    year_pain_began = models.CharField(
        max_length=20, blank=True, null=True, default="")
    onset_of_pain = models.CharField(
        max_length=20, blank=True, null=True, default="")
    gender = models.CharField(max_length=20)
    comments = models.TextField(blank=True, null=True, default="")

    often_pain = models.CharField(
        max_length=20, blank=True, null=True, default="")
    no_pain = models.CharField(
        max_length=20, blank=True, null=True, default="")
    pain_free = models.CharField(
        max_length=20, blank=True, null=True, default="")
    time_of_pain_best = models.CharField(
        max_length=20, blank=True, null=True, default="")
    time_of_pain_worst = models.CharField(
        max_length=20, blank=True, null=True, default="")
    increase_pain_comments = models.TextField(
        blank=True, null=True, default="")
    decrease_pain_comments = models.TextField(
        blank=True, null=True, default="")
    relieve_pain_comments = models.TextField(blank=True, null=True, default="")
    trouble_sleep = models.CharField(
        max_length=20, blank=True, null=True, default="")
    medication_sleep = models.CharField(
        max_length=20, blank=True, null=True, default="")
    awake_pain = models.CharField(
        max_length=20, blank=True, null=True, default="")
    present_pain_comments = models.TextField(blank=True, null=True, default="")

    scans = models.CharField(max_length=20, blank=True, null=True, default="")
    blood_tests = models.CharField(
        max_length=20, blank=True, null=True, default="")
    nerve_tests = models.CharField(
        max_length=20, blank=True, null=True, default="")
    x_rays = models.CharField(max_length=20, blank=True, null=True, default="")
    scan_professional = models.CharField(
        max_length=20, blank=True, null=True, default="")
    scan_hospital = models.CharField(
        max_length=20, blank=True, null=True, default="")
    blood_professional = models.CharField(
        max_length=20, blank=True, null=True, default="")
    blood_hospital = models.CharField(
        max_length=20, blank=True, null=True, default="")
    nerve_professional = models.CharField(
        max_length=20, blank=True, null=True, default="")
    nerve_hospital = models.CharField(
        max_length=20, blank=True, null=True, default="")
    x_rays_professional = models.CharField(
        max_length=20, blank=True, null=True, default="")
    x_rays_hospital = models.CharField(
        max_length=20, blank=True, null=True, default="")
    major_illness_comments = models.TextField(
        blank=True, null=True, default="")
    other_llness_comments = models.TextField(blank=True, null=True, default="")
    mentalservices = models.CharField(
        max_length=20, blank=True, null=True, default="")
    mental_support = models.CharField(
        max_length=20, blank=True, null=True, default="")
    injections = models.CharField(
        max_length=20, blank=True, null=True, default="")
    psychology = models.CharField(
        max_length=20, blank=True, null=True, default="")
    physiotherapy = models.CharField(
        max_length=20, blank=True, null=True, default="")
    tens = models.CharField(max_length=20, blank=True, null=True, default="")
    acupuncture = models.CharField(
        max_length=20, blank=True, null=True, default="")
    chiropractor = models.CharField(
        max_length=20, blank=True, null=True, default="")
    collars = models.CharField(
        max_length=20, blank=True, null=True, default="")
    wheel_chair = models.CharField(
        max_length=20, blank=True, null=True, default="")
    other_treatments = models.CharField(
        max_length=20, blank=True, null=True, default="")
    treatment_details_comments = models.TextField(
        blank=True, null=True, default="")
    smoke = models.CharField(max_length=20, blank=True, null=True, default="")
    smoke_day = models.CharField(
        max_length=20, blank=True, null=True, default="")
    alcohol = models.CharField(
        max_length=20, blank=True, null=True, default="")
    alcohol_day = models.CharField(
        max_length=20, blank=True, null=True, default="")
    physical_activity_comments = models.TextField(
        blank=True, null=True, default="")
    spend_day_comments = models.TextField(blank=True, null=True, default="")

    mood_changed = models.CharField(
        max_length=20, blank=True, null=True, default="")
    ways_relax = models.CharField(
        max_length=20, blank=True, null=True, default="")

    class Meta:
        db_table = "pain_details"


class Medications(models.Model):
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=100, blank=True, null=True)
    medication_dose = models.CharField(max_length=100, blank=True, null=True)
    medication_frequency = models.CharField(max_length=100, blank=True, null=True)
    other_medication = models.CharField(max_length=100, blank=True, null=True)
    medication_details = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="inactive")

    class Meta:
        db_table = "medications"


class PersonalDetails(models.Model):
    patient_fk = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    alone = models.CharField(max_length=20,blank=True,null=True)
    martual_status = models.CharField(max_length=20,blank=True,null=True)   
    number_children = models.CharField(max_length=20,blank=True,null=True)   
    number_children_home = models.CharField(max_length=20,blank=True,null=True)   
    current_situtaion = models.CharField(max_length=20,blank=True,null=True)   
    job_title = models.CharField(max_length=20,blank=True,null=True)   
    stop_working = models.CharField(max_length=20,blank=True,null=True)   
    legal_actions = models.CharField(max_length=20,blank=True,null=True)  

    class Meta:
        db_table = "personal_details" 
