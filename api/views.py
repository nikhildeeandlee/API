
import json
from django.forms import model_to_dict
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.response import Response

from datetime import datetime

from .send_mail import send_email_verification_mail, send_forget_password_mail

from rest_framework import generics, status, response

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import jwt
import datetime


# Create your views here.


# Patient Register
@api_view(['POST'])
def patient_register(request):
    print("python register")
    patient_data = JSONParser().parse(request)
    patient_serializer = PatientRegSerializer(data=patient_data)

    user_exist = PatientRegister.objects.filter(
        username=patient_data['username'])
    email_exist = PatientRegister.objects.filter(email=patient_data['email'])

    email = patient_data['email']
    username = patient_data['username']
    password1 = patient_data['password1']
    password2 = patient_data['password2']

    try:

        if patient_serializer.is_valid():

            if user_exist:
                return JsonResponse({'message': 'Username already exist'})

            if email_exist:
                return JsonResponse({'message': 'Email already exist'})

            if password1 == password2:
                user = patient_serializer.save()
                payload = {
                    'id': user.patient_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                auth_token = jwt.encode(payload, 'secret', algorithm='HS256')
                account = PatientRegister.objects.get(username=username)
                account.auth_token = auth_token
                account.save()

                verify_link = f'http://localhost:3000/verify/{auth_token}'

                send_email_verification_mail(email, verify_link)

                data = [patient_serializer.data]
                response = Response()
                response.set_cookie(key='jwt', value=auth_token, httponly=True)
                response.data = {
                    "status": True,
                    "status_code": status.HTTP_200_OK,
                    "message": "success",
                    "auth_token": auth_token,
                    "register_details": "patient",
                    "data": data,
                }
                return response

            else:
                return JsonResponse({'message': 'Password does not match'})

        return JsonResponse(patient_serializer.errors)

    except Exception as e:
        print(e)


# Patient Login
@api_view(['POST'])
def patient_login(request):

    patient_data = JSONParser().parse(request)
    patient_serializer = PatientLoginSerializer(data=patient_data)

    user_name = patient_data['username']
    password = patient_data['password1']

    if '@' in user_name:
        user_exist = PatientRegister.objects.filter(
            email=user_name, password1=password).first()

    else:
        user_exist = PatientRegister.objects.filter(
            username=user_name, password1=password).first()

    if patient_serializer.is_valid():
        if user_exist:
            if not user_exist.is_verified:
                return JsonResponse({
                    "message": "Your account is not verified check your mail."
                })
            current_datetime = datetime.datetime.now()

            patient_serializer.time_stamp = current_datetime
            time_stamp = patient_serializer.time_stamp
            PatientRegister.objects.filter(
                username=user_name).update(time_stamp=time_stamp)

            if '@' in user_name:
                id = PatientRegister.objects.filter(
                    email=user_name, password1=password).first()
            else:
                id = PatientRegister.objects.filter(
                    username=user_name, password1=password).first()

            user_id = id.patient_id
            data = [patient_serializer.data]
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
                'id': user_id,
                'data': data,
            })

        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(patient_serializer.errors)


# Patient Update
@api_view(['PUT'])
def patient_update(request, id):

    patient_data = PatientRegister.objects.get(
        patient_id=id)
    patient_serializer = PatientUpdateSerializer(
        instance=patient_data, data=request.data)

    queryset = PatientRegister.objects.filter(email=request.data['email'])

    if patient_serializer.is_valid():
        if not queryset:
            patient_serializer.save()
        elif patient_serializer.is_valid():
            if patient_data.email == request.data['email']:
                patient_serializer.save()
            else:
                return JsonResponse({"message": "email already exists"})
        return JsonResponse(patient_serializer.data)

    return JsonResponse(patient_serializer.errors)


# forget password link creating for patient
class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = PatientForgetPasswordSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        patient = PatientRegister.objects.filter(email=email).first()

        if patient:

            payload = {
                'id': patient.patient_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            encoded_pk = urlsafe_base64_encode(force_bytes(patient.patient_id))
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            print("password token", reset_url)

            patient.reset_token = token
            patient.save()

            reset_link = f"http://localhost:3000/ChangePassword{reset_url}"
            send_email = PatientRegister.objects.get(email=email).email
            send_forget_password_mail(send_email, reset_link)

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                "status": status.HTTP_200_OK,
                "message": "success",
                "encoded_pk": encoded_pk,
                "token": token,
                "reset_link": reset_link,
            }
            return response
        else:
            return JsonResponse(
                {
                    "message": "User doesn't exists"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# Changing Password
class ChangePassword(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = PatientChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        if serializer.is_valid(raise_exception=True):
            return response.Response(
                {
                    "message": "success"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(serializer.errors)


# Email verification for patient
@api_view(['POST'])
def verify(request, auth_token):

    try:
        patient_obj = PatientRegister.objects.filter(
            auth_token=auth_token).first()

        if patient_obj:
            print("patient obj true")
            if patient_obj.is_verified:
                print("patient already verified")
                return response.Response(
                    {
                        "message": "Your account is already verified.",
                        "login_details": "patient",
                    }
                )
            else:
                patient_obj.is_verified = True
                patient_obj.save()
                print("patient verified")
            return response.Response(
                {
                    "message": "Your account has been verified.",
                    "login_details": "patient",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {
                    "message": "Link is invalid or expired"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        print(e)


# Tech Support Register
@api_view(['POST'])
def tech_register(request):

    tech_data = JSONParser().parse(request)
    tech_serializer = TechRegSerializer(data=tech_data)

    queryset = TechRegister.objects.filter(
        Q(username=tech_data['username']) | Q(email=tech_data['email']))

    password1 = tech_data['password1']
    password2 = tech_data['password2']

    if tech_serializer.is_valid():
        if not queryset:
            if password1 == password2:
                tech_serializer.save()
                return JsonResponse({'message': 'Registered successfully'})
            else:
                return JsonResponse({'message': 'Password does not match'})
        else:
            return JsonResponse({'message': 'Email or Username already exist'})

    return JsonResponse(tech_serializer.errors)


# Tech Support Login
@api_view(['POST'])
def tech_login(request):

    tech_data = JSONParser().parse(request)
    tech_serializer = TechLoginSerializer(data=tech_data)

    user_name = tech_data['username']
    password = tech_data['password1']

    if '@' in user_name:
        user_exist = TechRegister.objects.filter(
            email=user_name, password1=password).exists()

    else:
        user_exist = TechRegister.objects.filter(
            username=user_name, password1=password).exists()

    if tech_serializer.is_valid():
        if user_exist:
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(tech_serializer.errors)


# Tech Details Display
@api_view(['GET'])
def tech_display(request):
    tech_data = TechRegister.objects.all()
    json_data = [{'id': i.tech_id, 'name': i.name, 'username': i.username,
                  'email': i.email, 'phone_number': i.phone_number, 'address': i.address, 'password1': i.password1, 'password2': i.password2, }for i in tech_data]
    return JsonResponse({'message': json_data})


# Doctor Register
@api_view(['POST'])
def doctor_register(request):

    doctor_data = JSONParser().parse(request)
    doctor_serializer = DoctorRegSerializer(data=doctor_data)

    user_exist = DoctorRegister.objects.filter(
        username=doctor_data['username'])

    email_exist = DoctorRegister.objects.filter(email=doctor_data['email'])

    email = doctor_data['email']
    username = doctor_data['username']
    password1 = doctor_data['password1']
    password2 = doctor_data['password2']

    try:

        if doctor_serializer.is_valid():
            if user_exist:
                return JsonResponse({'message': 'Username already exist'})

            if email_exist:
                return JsonResponse({'message': 'Email already exist'})
            if password1 == password2:
                user = doctor_serializer.save()
                payload = {
                    'id': user.doctor_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                auth_token = jwt.encode(payload, 'secret', algorithm='HS256')
                account = DoctorRegister.objects.get(username=username)
                account.auth_token = auth_token
                account.save()

                verify_link = f'http://localhost:3000/doctor-verify/{auth_token}'

                send_email_verification_mail(email, verify_link)

                data = [doctor_serializer.data]
                response = Response()
                response.set_cookie(key='jwt', value=auth_token, httponly=True)
                response.data = {
                    "status": True,
                    "status_code": status.HTTP_200_OK,
                    "message": "success",
                    "auth_token": auth_token,
                    "register_details": "doctor",
                    "data": data,
                }
                return response

            else:
                return JsonResponse({'message': 'Password does not match'})

        return JsonResponse(doctor_serializer.errors)

    except Exception as e:
        print(e)

# Doctor Login


@api_view(['POST'])
def doctor_login(request):

    doctor_data = JSONParser().parse(request)
    doctor_serializer = DoctorLoginSerializer(data=doctor_data)

    user_name = doctor_data['username']
    password = doctor_data['password1']

    if '@' in user_name:
        user_exist = DoctorRegister.objects.filter(
            email=user_name, password1=password).first()

    else:
        user_exist = DoctorRegister.objects.filter(
            username=user_name, password1=password).first()

    if doctor_serializer.is_valid():
        if user_exist:
            if not user_exist.is_verified:
                return JsonResponse({
                    "message": "Your account is not verified check your mail."
                })
            else:
                current_datetime = datetime.datetime.now()
                doctor_serializer.time_stamp = current_datetime
                time_stamp = doctor_serializer.time_stamp
                DoctorRegister.objects.filter(
                    username=user_name).update(time_stamp=time_stamp)

            if '@' in user_name:
                id = DoctorRegister.objects.filter(
                    email=user_name, password1=password).first()
            else:
                id = DoctorRegister.objects.filter(
                    username=user_name, password1=password).first()

            user_id = id.doctor_id
            data = [doctor_serializer.data]
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
                'id': user_id,
                'data': data,
            })

        else:
            return JsonResponse({'message': 'Please enter a vaild details'})
    return JsonResponse(doctor_serializer.errors)


# Doctor Details Display
@api_view(['GET'])
def doctor_display(request, id):
    # doctor Details
    doctor_details = DoctorRegister.objects.get(doctor_id=id)
    doctor_details_data = {}

    if doctor_details:
        doctor_details_data = model_to_dict(doctor_details, fields=[
            'firstname', 'lastname', 'username',
            'specialization', 'hospital_id', 'email', 'phone_number', 'password1', 'password2'])
    print("doctor details = ", doctor_details_data)

    return Response({
        'doctor_details': doctor_details_data,
    })


# Email verification for doctor
@api_view(['POST'])
def doctor_verify(request, auth_token):

    try:
        doctor_obj = DoctorRegister.objects.filter(
            auth_token=auth_token).first()

        if doctor_obj:
            print("doctor obj true")
            if doctor_obj.is_verified:
                print("doctor already verified")
                return response.Response(
                    {
                        "message": "Your account is already verified.",
                        "login_details": "doctor",
                    }
                )
            else:
                doctor_obj.is_verified = True
                doctor_obj.save()
                print("doctor verified")
            return response.Response(
                {
                    "message": "Your account has been verified.",
                    "login_details": "doctor",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {
                    "message": "Link is invalid or expired"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        print(e)


# Pain Questions
@api_view(['POST'])
def pain_selection(request, id):
    selection_data = JSONParser().parse(request)

    question_selection = selection_data.keys()

    pain_Start = selection_data['pain_start']
    discribe_pain = selection_data['discribe_pain']

    print('pain start = ', pain_Start)
    print('discribe pain = ', discribe_pain)

    for i in question_selection:  # questions
        print("questions", i)

        qsn = PainQuestions.objects.get(questions=i)

        update = PainSelection.objects.filter(
            patient_fk=id, question_fk=qsn.id)
        for upd in update:

            PainSelection.objects.filter(
                patient_fk=id, question_fk=qsn.id).update(key=False)

        if i == "pain_start":
            for start in pain_Start:
                pain_start_answers = PainAnswers.objects.filter(answers=start)
                patient_fk = id

                if pain_start_answers:
                    question_obj = PainQuestions.objects.get(questions=i)
                    answer_obj = PainAnswers.objects.get(answers=start)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    pain_selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)

                    pain_selection.save()
                else:
                    return JsonResponse({"message": "Pain start answers does not match"})

        if i == "discribe_pain":
            for discribe in discribe_pain:
                discribe_pain_answers = PainAnswers.objects.filter(
                    answers=discribe)
                patient_fk = id

                if discribe_pain_answers:
                    question_obj = PainQuestions.objects.get(questions=i)
                    answer_obj = PainAnswers.objects.get(answers=discribe)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    pain_selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)
                    pain_selection.save()

                else:
                    return JsonResponse({"message": "Discribe pain answers does not match"})
        else:
            print("not discribe pain")

    return JsonResponse({
        'status': True,
        'status_code': status.HTTP_200_OK,
        'message': 'success',

    })


# Pain details
@api_view(['POST'])
def pain_details(request, id):

    details_data = JSONParser().parse(request)
    serializer = PainDetailsSerializer(data=details_data)
    obj = PainDetails.objects.filter(patient_fk=id).first()
    year_pain_began = details_data['year_pain_began']
    onset_of_pain = details_data['onset_of_pain']
    gender = details_data['gender']
    comments = details_data['comments']

    if serializer.is_valid():
        if not obj:
            serializer.patient_fk_id = id
            fk = serializer.patient_fk_id
            serializer.save(patient_fk_id=fk)

            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })

        else:
            PainDetails.objects.filter(patient_fk=id).update(
                year_pain_began=year_pain_began, onset_of_pain=onset_of_pain, gender=gender, comments=comments)
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
    return JsonResponse(serializer.errors)


@api_view(['PUT'])
def present_pain_pattern(request, id):

    obj = PainDetails.objects.get(patient_fk=id)
    serializer = PresentPainPatternSerializer(
        instance=obj, data=request.data)

    no_pain = request.data['no_pain']
    pain_free = request.data['pain_free']
    try:

        if serializer.is_valid():
            if no_pain == 'No':
                pain_free = ""
            serializer.save(pain_free=pain_free)
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
        else:
            return JsonResponse(serializer.errors)
    except Exception as e:
        print(e)


# Pain investigation checkbox
@api_view(['POST'])
def pain_investigation_checkbox(request, id):

    # Pain Investigation checkboxes
    selection_data = JSONParser().parse(request)

    question_selection = "pain_investigation"
    print("adfadfadafasfd", question_selection)
    pain_investigation = selection_data['pain_investigation']

    print('pain investigation = ', pain_investigation)

    qsn = PainQuestions.objects.get(questions=question_selection)

    update = PainSelection.objects.filter(patient_fk=id, question_fk=qsn.id)
    try:
        for upd in update:

            PainSelection.objects.filter(
                patient_fk=id, question_fk=qsn.id).update(key=False)

        if question_selection == "pain_investigation":
            print("yes question is ", question_selection)
            for investigation in pain_investigation:
                pain_investigation_answers = PainAnswers.objects.filter(
                    answers=investigation)
                patient_fk = id

                if pain_investigation_answers:
                    question_obj = PainQuestions.objects.get(
                        questions=question_selection)
                    answer_obj = PainAnswers.objects.get(answers=investigation)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    pain_selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)

                    pain_selection.save()
                    print("saved")
                else:
                    return JsonResponse({"message": "Answers does not match"})

            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
    except Exception as e:
        print(e)


# Pain Investigation
@api_view(['POST'])
def pain_investigation(request, id):
    # pain investigation other fields
    obj = PainDetails.objects.get(patient_fk=id)
    serializer = PainInvestigation_Serializer(
        instance=obj, data=request.data)

    scans = request.data['scans']
    scan_professional = request.data['scan_professional']
    scan_hospital = request.data['scan_hospital']

    blood_tests = request.data['blood_tests']
    blood_professional = request.data['blood_professional']
    blood_hospital = request.data['blood_hospital']

    nerve_tests = request.data['nerve_tests']
    nerve_professional = request.data['nerve_professional']
    nerve_hospital = request.data['nerve_hospital']

    x_rays = request.data['x_rays']
    x_rays_professional = request.data['x_rays_professional']
    x_rays_hospital = request.data['x_rays_hospital']

    mentalservices = request.data['mentalservices']
    mental_support = request.data['mental_support']
    smoke = request.data['smoke']
    smoke_day = request.data['smoke_day']
    alcohol = request.data['alcohol']
    alcohol_day = request.data['alcohol_day']

    # try:
    if serializer.is_valid():
        if scans == 'Awaiting' or 'Had Done':
            scan_professional = scan_professional
            scan_hospital = scan_hospital
        else:
            scan_professional = ""
            scan_hospital = ""
        if blood_tests == 'Awaiting' or 'Had Done':
            blood_professional = blood_professional
            blood_hospital = blood_hospital
        else:
            blood_professional = ""
            blood_professional = ""
        if nerve_tests == 'Awaiting' or 'Had Done':
            nerve_professional = nerve_professional
            nerve_hospital = nerve_hospital
        else:
            nerve_professional = ""
            nerve_hospital = ""
        if x_rays == 'Awaiting' or 'Had Done':
            x_rays_professional = x_rays_professional
            x_rays_hospital = x_rays_hospital
        else:
            x_rays_professional = ""
            x_rays_hospital = ""

        if mentalservices == 'Yes':
            mental_support = mental_support
        else:
            mental_support = ""
        if smoke == 'Yes':
            smoke_day = smoke_day
        else:
            smoke_day = ""
        if alcohol == 'Yes':
            alcohol_day = alcohol_day
        else:
            alcohol_day = ""

        serializer.save(scan_professional=scan_professional, scan_hospital=scan_hospital,
                        blood_professional=blood_professional, blood_hospital=blood_hospital,
                        nerve_professional=nerve_professional, nerve_hospital=nerve_hospital,
                        x_rays_professional=x_rays_professional, x_rays_hospital=x_rays_hospital,
                        mental_support=mental_support, smoke_day=smoke_day, alcohol_day=alcohol_day)
        print("saved pain investigation")
        return JsonResponse({
            'status': True,
            'status_code': status.HTTP_200_OK,
            'message': 'success',
            'data': serializer.data,
        })
    else:
        JsonResponse(serializer.errors)


@api_view(['POST'])
def regular_medication(request, id):

    regularmedications = JSONParser().parse(request)
    medication_details = "regular medication"

    regular = regularmedications['regularmedications']

    # Medications.objects.filter(
    #     patient_fk=id, medication_details=medication_details).update(status="inactive")

    num = 1
    for medication in regular:
        print(medication)
        medi_name = f'medication_M{num}'
        medi_dose = f'medication_D{num}'
        medi_frequency = f'medication_F{num}'

        medication_name = medication.get(medi_name)
        medication_dose = medication.get(medi_dose)
        medication_frequency = medication.get(medi_frequency)
        medi_type = medication.get('medication_type')
        other_medication = medication.get('other_medication')

        print(medication_name)
        print(medication_dose)
        print(medication_frequency)
        num = num+1
        if medi_type == 'regular_medication':
            medication_save = Medications(patient_fk_id=id, medication_name=medication_name, medication_dose=medication_dose,
                                          medication_frequency=medication_frequency, medication_details=medi_type, status="active")
            medication_save.save()
        if medi_type == 'as_now_medication':
            medication_save = Medications(patient_fk_id=id, medication_name=medication_name, medication_dose=medication_dose,
                                          medication_frequency=medication_frequency, medication_details=medi_type, status="active")
            medication_save.save()
        if medi_type == 'past_medication':
            medication_save = Medications(patient_fk_id=id, medication_name=medication_name, medication_dose=medication_dose,
                                          medication_frequency=medication_frequency, medication_details=medi_type, status="active")
            medication_save.save()
        if medi_type == 'other_medication':
            medication_save = Medications(
                patient_fk_id=id, other_medication=other_medication, medication_details=medi_type, status="active")
            medication_save.save()
    return JsonResponse({
        'status': True,
        'status_code': status.HTTP_200_OK,
        'message': 'success',
        'data': regularmedications,

    })


# Pain other effect
@api_view(['POST'])
def pain_other_effect_checkbox(request, id):

    selection_data = JSONParser().parse(request)

    question_selection = "pain_associat"
    print("question selection", question_selection)
    pain_associat = selection_data['pain_associat']

    print('pain investigation = ', pain_associat)

    qsn = PainQuestions.objects.get(questions=question_selection)

    update = PainSelection.objects.filter(patient_fk=id, question_fk=qsn.id)
    try:

        for upd in update:

            PainSelection.objects.filter(
                patient_fk=id, question_fk=qsn.id).update(key=False)

        if question_selection == "pain_associat":
            print("yes question is ", question_selection)
            for associat in pain_associat:
                pain_investigation_answers = PainAnswers.objects.filter(
                    answers=associat)
                patient_fk = id

                if pain_investigation_answers:
                    question_obj = PainQuestions.objects.get(
                        questions=question_selection)
                    answer_obj = PainAnswers.objects.get(answers=associat)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)

                    selection.save()
                    print("saved")
                else:
                    return JsonResponse({"message": "Answers does not match"})

            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
    except Exception as e:
        print(e)


# Pain other effect
@api_view(['POST'])
def pain_other_effect(request, id):
    # pain other effect other fields
    obj = PainDetails.objects.get(patient_fk=id)
    serializer = pain_other_effect_serializer(
        instance=obj, data=request.data)

    # try:
    if serializer.is_valid():
        serializer.save()
        print("saved other effect")
        return JsonResponse({
            'status': True,
            'status_code': status.HTTP_200_OK,
            'message': 'success',
            'data': serializer.data,
        })
    else:
        JsonResponse(serializer.errors)


# Personal Details
@api_view(['POST'])
def personal_details(request, id):

    personal_data = JSONParser().parse(request)
    serializer = PersonalDetailsSerializer(data=personal_data)
    obj = PersonalDetails.objects.filter(patient_fk=id).first()

    alone = personal_data['alone']
    martual_status = personal_data['martual_status']
    number_children = personal_data['number_children']
    number_children_home = personal_data['number_children_home']
    current_situtaion = personal_data['current_situtaion']
    job_title = personal_data['job_title']
    stop_working = personal_data['stop_working']
    legal_actions = personal_data['legal_actions']

    if serializer.is_valid():
        if not obj:
            serializer.patient_fk_id = id
            fk = serializer.patient_fk_id
            serializer.save(patient_fk_id=fk)

            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })

        else:
            PersonalDetails.objects.filter(patient_fk=id).update(
                alone=alone, martual_status=martual_status, number_children=number_children, number_children_home=number_children_home, current_situtaion=current_situtaion, job_title=job_title, stop_working=stop_working, legal_actions=legal_actions)
            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
    return JsonResponse(serializer.errors)


# Personal details checkboxes
@api_view(['POST'])
def personal_details_checkbox(request, id):

    selection_data = JSONParser().parse(request)

    question_selection = "state_benfits"
    print("question selection", question_selection)
    state_benfits = selection_data['state_benfits']

    print('state benfits = ', state_benfits)

    qsn = PainQuestions.objects.get(questions=question_selection)

    try:
        print("aaaaaaaaaa")
        update = PainSelection.objects.filter(
            patient_fk=id, question_fk=qsn.id)
        print("bbbbbbbbb")
        if update:

            for upd in update:

                PainSelection.objects.filter(
                    patient_fk=id, question_fk=qsn.id).update(key=False)
        print("ccccccccccccc")
        if question_selection == "state_benfits":
            print("yes question is ", question_selection)
            for benfits in state_benfits:
                state_benfits_answers = PainAnswers.objects.filter(
                    answers=benfits)
                patient_fk = id

                if state_benfits_answers:
                    question_obj = PainQuestions.objects.get(
                        questions=question_selection)
                    answer_obj = PainAnswers.objects.get(answers=benfits)
                    question_fk = question_obj.id
                    answer_fk = answer_obj.id
                    key = True
                    current_datetime = datetime.datetime.now()

                    selection = PainSelection(
                        patient_fk_id=patient_fk, question_fk_id=question_fk, answer_fk_id=answer_fk, key=key, time_stamp=current_datetime)

                    selection.save()
                    print("saved")
                else:
                    return JsonResponse({"message": "Answers does not match"})

            return JsonResponse({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'success',
            })
    except Exception as e:
        print(e)


# Get API for all pages
@api_view(['GET'])
def patient_display(request, id):

    data = {}
    # Patient Details
    patient_details = PatientRegister.objects.get(patient_id=id)
    patient_details_data = {}

    if patient_details:
        patient_details_data = model_to_dict(patient_details, fields=[
            'patient_id', 'firstname', 'lastname', 'phone_number', 'email', 'hospital_number', 'dateofbirth', 'address', 'postcode'])
    data['patient_details'] = patient_details_data

    # Pain start and discribe pain
    pain_start = PainQuestions.objects.filter(questions="pain_start").first()
    discribe_pain = PainQuestions.objects.filter(
        questions="discribe_pain").first()

    pain_start_selection = PainSelection.objects.filter(
        question_fk=pain_start.id, patient_fk=id, key=True)

    discribe_pain_selection = PainSelection.objects.filter(
        question_fk=discribe_pain.id, patient_fk=id, key=True)
    discribe_pain_selection = PainSelection.objects.filter(
        question_fk=discribe_pain.id, patient_fk=id, key=True)

    # Pain Start
    pain_start_dict = {}
    pain_start_data = []
    for i in pain_start_selection:
        print("pain start selection = ", i.answer_fk.answers)
        pain_start_dict['answers'] = i.answer_fk.answers
        pain_start_data.append(pain_start_dict['answers'])
    data['pain_start'] = pain_start_data

    # Discribe Pain
    discribe_pain_dict = {}
    discribe_pain_data = []
    for i in discribe_pain_selection:
        print("discribe pain selection = ", i.answer_fk.answers)
        discribe_pain_dict['answers'] = i.answer_fk.answers
        discribe_pain_data.append(discribe_pain_dict['answers'])
    data['discribe_pain'] = discribe_pain_data

    pain_details = PainDetails.objects.filter(patient_fk=id).first()
    pain_details_data = []
    present_pain_data = []
    pain_investigation_data = []
    pain_other_effect_data = []
    if pain_details:
        # Pain Details
        pain_details_data = model_to_dict(
            pain_details, fields=['year_pain_began', 'onset_of_pain', 'gender', 'comments'])
        data['pain_details'] = pain_details_data

        # Present pain
        present_pain_data = model_to_dict(
            pain_details, fields=['often_pain', 'no_pain', 'pain_free', 'time_of_pain_best', 'time_of_pain_worst', 'increase_pain_comments',
                                  'decrease_pain_comments', 'relieve_pain_comments', 'trouble_sleep', 'medication_sleep', 'awake_pain', 'present_pain_comments'])
        data['present_pain'] = present_pain_data

        # Pain investigation
        pain_investigation_data = model_to_dict(
            pain_details, fields=['scans', 'blood_tests', 'nerve_tests', 'x_rays', 'scan_professional', 'scan_hospital',
                                  'blood_professional', 'blood_hospital', 'nerve_professional', 'nerve_hospital', 'x_rays_professional', 'x_rays_hospital',
                                  'major_illness_comments', 'other_llness_comments', 'mentalservices', 'mental_support', 'injections', 'psychology',
                                  'physiotherapy', 'tens', 'acupuncture', 'chiropractor', 'collars', 'wheel_chair', 'other_treatments', 'treatment_details_comments', 'smoke',
                                  'smoke_day', 'alcohol', 'alcohol_day', 'physical_activity_comments', 'spend_day_comments'])
        data['pain_investigation'] = pain_investigation_data

        # Pain other effect
        pain_other_effect_data = model_to_dict(
            pain_details, fields=['mood_changed', 'ways_relax'])
        data['pain_other_effect'] = pain_investigation_data

    # Pain investigation checkbox
    pain_investigation_Checkbox_dict = {}
    pain_investigation_checkbox_data = []
    pain_investigation = PainQuestions.objects.filter(
        questions="pain_investigation").first()
    pain_investigation_selection = PainSelection.objects.filter(
        question_fk=pain_investigation.id, patient_fk=id, key=True)

    for i in pain_investigation_selection:
        print("pain investigation selection = ", i.answer_fk.answers)
        pain_investigation_Checkbox_dict['answers'] = i.answer_fk.answers
        pain_investigation_checkbox_data.append(
            pain_investigation_Checkbox_dict['answers'])
    data['pain_investigation_checkbox'] = pain_investigation_checkbox_data

    # Pain other effect
    pain_associat_Checkbox_dict = {}
    pain_associat_checkbox_data = []
    pain_associat = PainQuestions.objects.filter(
        questions="pain_associat").first()
    pain_associat_selection = PainSelection.objects.filter(
        question_fk=pain_associat.id, patient_fk=id, key=True)

    for i in pain_associat_selection:
        print("pain accociat selection = ", i.answer_fk.answers)
        pain_associat_Checkbox_dict['answers'] = i.answer_fk.answers
        pain_associat_checkbox_data.append(
            pain_associat_Checkbox_dict['answers'])
    data['pain_associat'] = pain_associat_checkbox_data

    # Regular medication
    regular_medication_dict = {}
    regular_medication_data = []
    regular_medication = Medications.objects.filter(
        patient_fk=id, medication_details="regular medication", status="active")

    # for medication in regular_medication:
    #    regular_medication_dict['regular_medications'] = medication
    #         print("regular medication = ", regular_medication_data)
    # data['medication'] = regular_medication_data

    # Personal details
    personal_details = PersonalDetails.objects.filter(patient_fk=id).first()
    personal_details_data = model_to_dict(
        personal_details, fields=['alone', 'martual_status', 'number_children', 'number_children_home', 'current_situtaion', 'job_title', 'stop_working', 'legal_actions'])
    data['personal_details'] = personal_details_data

    # Personal details checkbox
    personal_details_Checkbox_dict = {}
    personal_details_checkbox_data = []
    personal_details = PainQuestions.objects.filter(
        questions="state_benfits").first()
    personal_details_selection = PainSelection.objects.filter(
        question_fk=personal_details.id, patient_fk=id, key=True)

    for i in personal_details_selection:
        print("personal details selection = ", i.answer_fk.answers)
        personal_details_Checkbox_dict['answers'] = i.answer_fk.answers
        personal_details_checkbox_data.append(
            personal_details_Checkbox_dict['answers'])
    data['personal_details_checkbox'] = personal_details_checkbox_data

    return Response(data)




# forget password link creating for doctor
class PasswordResetDoctor(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = DoctotForgerPasswordSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        doctor = DoctorRegister.objects.filter(email=email).first()

        if doctor:

            payload = {
                'id': doctor.doctor_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            encoded_pk = urlsafe_base64_encode(force_bytes(doctor.doctor_id))
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            reset_url = reverse(
                "reset-password-doctor",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            print("password token", reset_url)

            doctor.reset_token = token
            doctor.save()

            # reset_link = f"http://localhost:3000/ChangePassword{reset_url}"
            reset_link = f"http://127.0.0.1:8000{reset_url}"
            send_email = DoctorRegister.objects.get(email=email).email
            send_forget_password_mail(send_email, reset_link)

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                "status": status.HTTP_200_OK,
                "message": "success",
                "encoded_pk": encoded_pk,
                "token": token,
                "reset_link": reset_link,
            }
            return response
        else:
            return JsonResponse(
                {
                    "message": "User doesn't exists"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# Changing Password Doctor
class ChangePasswordDoctor(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = DoctorChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        if serializer.is_valid(raise_exception=True):
            return response.Response(
                {
                    "message": "success"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(serializer.errors)
