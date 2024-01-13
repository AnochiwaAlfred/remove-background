from django.shortcuts import get_object_or_404, redirect
from ninja import Router, Schema
from decouple import config
from ninja import NinjaAPI, FormEx
import pyotp
from plugins.generate_otp import generate_otp
from users.models import *
from schemas.auth import *
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as contrib_logout
from django.contrib.auth import authenticate
from plugins.hasher import hasherGenerator
from datetime import datetime, timedelta, timezone
from typing import List, Union
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import smtplib, ssl
from email.message import EmailMessage
# from google_auth_oauthlib.flow import Flow
# from google_auth_oauthlib import flow as small_flow
# from  google.auth.transport.requests import AuthorizedSession


router = Router(tags=["Authentication"])




@router.get("/")
def get_user(request):
    auth = request.auth

    user = CustomUser.objects.all().filter(token=auth).get()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "code": user.code,
    }


@router.get("/getAllUsers/", response=List[AuthUserRetrievalSchema])
def getAllUsers(request):
    users = CustomUser.objects.all()
    return users


@router.get("/{user_id}/get/", response=Union[AuthUserRetrievalSchema, str])
def get_user_by_id(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return user

@router.post("/token/", auth=None)  # < overriding global auth
def get_token(request, username: str = FormEx(...), password: str = FormEx(...)):
    """
    This will be used as signup request.
    """
    user = authenticate(username=username, password=password)
    if user:
        hh = hasherGenerator()
        string_formatted = hh.get("token").decode("utf-8")
        hh.update(
            {
                # "rsa_duration": 24,
                "token": string_formatted
            }
        )
        CustomUser.objects.all().filter(id=user.id).update(**hh)
        return {"token": hh.get("token")}
    else:return {"token": False}
        # User is authenticated


@router.post("/register-via-email/", auth=None)
def register_user_with_email(
    request,
    password: str,
    passwordConfirm: str,
    user_data: AuthUserRegistrationSchema = FormEx(...),
):
    user = CustomUser.objects.create(**user_data.dict())
    if password==passwordConfirm:
        user.set_password(password)
        user.save()
    return {"message": f"Registration successful. ID --> {user.id} BKEND"}



@router.post("/send-OTP-Email/", auth=None)
def send_otp_email(request, email):
    userInstance = CustomUser.objects.filter(email=email)
    if userInstance.exists():
        generate_otp(email)
        user = userInstance[0]

        email_address = config('SMTP_EMAIL')
        email_password = config('SMTP_PASSWORD')
        port = 465  # This is the default SSL port

        # create email
        msg = EmailMessage()
        msg["Subject"] = "Your OTP for Email Verification"
        msg["From"] = email_address
        msg["To"] = user.email
        msg.set_content(f"Your SpotiPY OTP is: {user.otp}")
        
        if user.is_verified==False:
            # send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(email_address, email_password)
                server.send_message(msg)
            return {"Message": f"OTP Sent. Check email for OTP"}
        else:return {"Message": f"User already verified"}
    else:return {"Error": f"User {email} does not exist."}

@router.post("/send-OTP-SMS/", auth=None)
def send_otp_sms(request, email):
    userInstance = CustomUser.objects.filter(email=email)
    if userInstance.exists():
        generate_otp(email)
        user = userInstance[0]
        # Twilio account credentials
        TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
        TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")
        
        # Note that if Twilio fails, register for and use Bandwidth API
        
        # Create a Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        if user.is_verified==False:
            # Send the OTP SMS
            try:
                message = client.messages.create(
                    to=f"{user.phone}",
                    from_=TWILIO_PHONE_NUMBER,
                    body=f"Your SpotiPY OTP is: {user.otp}"
                )
                # Print the message ID
                print(message.sid)
                return {"Message": f"OTP Sent. Check sms for OTP"}
            except TwilioRestException as e:
                return {"error": f"Error sending OTP: {e}"}
        else:return {"Message": f"User already verified"}
    else:return {"Error": f"User {email} does not exist."}

@router.post("/verify-otp/", auth=None)
def verify_otp(request, email: str, otp: str):
    user = CustomUser.objects.get(email=email)
    totp = pyotp.TOTP(user.otp)
    if not totp.verify(otp):
        return {"error": "Invalid OTP. Please try again."}

    user_otp_created_at = user.otp_created_at
    utc_otp_created_at = user_otp_created_at.replace(tzinfo=timezone.utc)
    
    if utc_otp_created_at < datetime.now(timezone.utc) - timedelta(minutes=5):
        return {"Message": "OTP has expired. Please request a new one."}
    else:
    # if totp.verify(otp):
        if otp==user.otp:
            user.is_verified = True
            user.is_active = True
            user.otp = ""
            user.save()
            return {"Message": "Email verification successful."}
        else:
            return {"Message": "Invalid OTP. Please try again."}
    


@router.post("/requestForgotPassword/{email}/", auth=None)
def request_forgot_password(request, email:str):
    userInstance = CustomUser.objects.filter(email=email)
    if userInstance.exists():
        generate_otp(email)
        user = userInstance[0]

        email_address = config('SMTP_EMAIL')
        email_password = config('SMTP_PASSWORD')
        port = 465  # This is the default SSL port

        # create email
        msg = EmailMessage()
        msg["Subject"] = "Your OTP for Email Verification"
        msg["From"] = email_address
        msg["To"] = user.email
        msg.set_content(f"Your SpotiPY OTP is: {user.otp}")
        
        # send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email_address, email_password)
            server.send_message(msg)
        return {"Message": f"OTP Sent. Check email for OTP"}
    else:return {"Error": f"User {email} does not exist."}


@router.post("/resetForgotPassword/{email}/", auth=None)
def reset_forgot_password(request, email:str, otp:str, password1:str, password2:str):
    userInstance = CustomUser.objects.filter(email=email)
    if userInstance.exists():
        user = userInstance[0]
        totp = pyotp.TOTP(user.otp)
        if not totp.verify(otp):
            return {"Error": "Invalid OTP. Please try again."}

        user_otp_created_at = user.otp_created_at
        utc_otp_created_at = user_otp_created_at.replace(tzinfo=timezone.utc)
        
        if utc_otp_created_at < datetime.now(timezone.utc) - timedelta(minutes=5):
            return {"Message": "OTP has expired. Please request a new one."}
        
        if otp==user.otp:
            if password1==password2:
                user.set_password(password1)
                user.is_verified = True
                user.is_active = True
                user.otp = ""
                user.save()
                return {"Message": "Email verification successful."}
            else:return {"Error":"Password mismatch"}
        else:return {"Error": "Invalid OTP. Please try again."}
        
        
@router.post("/logout/{token}")
def logout(request, token):
    user = CustomUser.objects.filter(token=token)[0]
    user.logout()
    contrib_logout(request)
    user.clear_token()
    return {
        "message": "User Logged Out; You can sign in again using your username and password."
    }


@router.post("createSuperUser/", response=AuthUserRetrievalSchema)
def createSuperUser(
    request, password: str, data: AuthUserRegistrationSchema = FormEx(...)
):
    authuser = CustomUser.objects.create(**data.dict())
    if authuser:
        authuser.set_password(password)
        authuser.is_active = True
        authuser.is_staff = True
        authuser.is_superuser = True
        authuser.save()
    return authuser

User = get_user_model()



@router.post("/login")
def login_user(request, email: str, password: str):
    validate = CustomUser.objects.filter(email=email)
    if validate:
        validated = validate[0].username
        user = authenticate(request, username=validated, password=password)
        if user:
            login(request, user)
            hh = hasherGenerator()
            access_token = hh.get("token").decode("utf-8")
            # tokenDict={"token":access_token}
            # CustomUser.objects.all().filter(id=user.id).update(**tokenDict)
            user2 = CustomUser.objects.filter(id=user.id)[0]
            user2.set_token(access_token)
            token=user2.token
            user2.login()
            return {"access_token": token, "user_id":user.id, "username":user2.username, "email":user2.email, "message":'Logged in Successfully BKEND'}
        else:
            return {"message": "Invalid password BKEND"}
    else:
        return {"message": "Invalid Email BKEND"}


@router.delete("/deleteUser/{user_id}/")
def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return f"User {user.username} deleted successfully"


           

