from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


# Patient Register Serializer
class PatientRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['firstname', 'lastname', 'username',
                  'email', 'phone_number', 'password1', 'password2']


# Patient Login Serializer
class PatientLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['username', 'password1', 'time_stamp']


# Change password serializer patient
class PatientChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['password1', 'password2']

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        newpassword = data.get("password1")
        confirmpassword = data.get("password2")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")
        print("token",token)
        print("encoded pk",encoded_pk)

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        patient = PatientRegister.objects.filter(patient_id=pk).first()

        check_token = PatientRegister.objects.get(reset_token=token)

        if not check_token:
            raise serializers.ValidationError("The reset token is invalid")
        else:
            if newpassword != confirmpassword:
                raise serializers.ValidationError("Password does not match")
            else:
                patient.password1 = newpassword
                patient.password2 = confirmpassword
                patient.save()
                print("password changed")
        return data


# Forget Password serializer
class PatientForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['email']


class DoctotForgerPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegister
        fields = ['email']


# Change password serializer doctor
class DoctorChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegister
        fields = ['password1', 'password2']

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        newpassword = data.get("password1")
        confirmpassword = data.get("password2")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")
        print("token",token)
        print("encoded pk",encoded_pk)

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        doctor = DoctorRegister.objects.filter(doctor_id=pk).first()
        print("working 1")
        check_token = DoctorRegister.objects.filter(reset_token=token).first()
        if not check_token:
            raise serializers.ValidationError("The reset token is invalid")
        else:
            if newpassword != confirmpassword:
                raise serializers.ValidationError("Password does not match")
            else:
                doctor.password1 = newpassword
                doctor.password2 = confirmpassword
                doctor.save()
                print("password changed")
        return data



# Patient Update Serializer
class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRegister
        fields = ['firstname', 'lastname',  'phone_number', 'dateofbirth',
                  'email', 'hospital_number', 'address', 'postcode']


# Tech Support Register Serializer
class TechRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechRegister
        fields = ['name', 'username', 'email', 'phone_number',
                  'address', 'password1', 'password2']


# Tech Support Login Serializer
class TechLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechRegister
        fields = ['username', 'password1']


# Doctor Register Serializer
class DoctorRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegister
        fields = ['firstname', 'lastname', 'username',
                  'specialization', 'hospital_id', 'email', 'phone_number', 'password1', 'password2']


# Doctor Login Serializer
class DoctorLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegister
        fields = ['username', 'password1']


# Pain Details Serializer
class PainDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PainDetails
        fields = ['year_pain_began', 'onset_of_pain', 'gender', 'comments']


# Present pain pattern serializer
class PresentPainPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = PainDetails
        fields = ['often_pain', 'no_pain', 'pain_free', 'time_of_pain_best', 'time_of_pain_worst', 'increase_pain_comments',
                  'decrease_pain_comments', 'relieve_pain_comments', 'trouble_sleep', 'medication_sleep', 'awake_pain', 'present_pain_comments']


# Pain Investigation Serializer
class PainInvestigation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PainDetails
        fields = ['scans', 'blood_tests', 'nerve_tests', 'x_rays', 'scan_professional', 'scan_hospital',
                  'blood_professional', 'blood_hospital', 'nerve_professional', 'nerve_hospital', 'x_rays_professional', 'x_rays_hospital',
                  'major_illness_comments', 'other_llness_comments', 'mentalservices', 'mental_support', 'injections', 'psychology',
                  'physiotherapy', 'tens', 'acupuncture', 'chiropractor', 'collars', 'wheel_chair', 'other_treatments', 'treatment_details_comments', 'smoke',
                  'smoke_day', 'alcohol', 'alcohol_day', 'physical_activity_comments', 'spend_day_comments']




# pain other effect
class pain_other_effect_serializer(serializers.ModelSerializer):
    class Meta:
        model = PainDetails
        fields = ['mood_changed','ways_relax']


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = ['alone','martual_status','number_children','number_children_home','current_situtaion','job_title','stop_working','legal_actions']
