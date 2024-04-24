import os, secrets
from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User, Link
from .serializers import Userserializer, ChangePasswordSerializer, Profileserializer
from rest_framework_simplejwt.tokens import RefreshToken


class Register(APIView):
    def post(self, request):
        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=make_password(request.data['password']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    

class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.get(username=username)
        if not user:
            return Response("User does not exist")
        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'message':'Login successful','token':token},status=status.HTTP_202_ACCEPTED)
        else:
            return Response("wrong password")
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        logout(request, user)
        return Response(status=status.HTTP_200_OK)
    

class Manageprofile(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = request.user
        serializer = Profileserializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response('Your account deleted successfully', status=status.HTTP_200_OK)
    
    
    def get(self,request):
        user = request.user
        serializer = Profileserializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not check_password(serializer.data.get('old_password'),user.password):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get('new_password') != serializer.data.get('confirm_new_password'):
                return Response({'error': 'new_password and confirm_new_password'}, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Forgetpassword(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        try:
            user1 = Link.objects.get(user_id=user.id)
        except Link.DoesNotExist:
                Link.objects.create(user_id=user.id)
        expires = timezone.now() + timedelta(seconds = 90)
        token = secrets.token_urlsafe(4)
        encoded_email_id = urlsafe_base64_encode(email.encode())
        Reset_link = (encoded_email_id) + '.' + (token)
        subject = 'Reset Your Password'
        message = "Hey ," + user.username + \
                    " To reset your password. Your link is :}"+ (Reset_link)
        email_from = os.getenv('EMAIL_HOST_USER')
        recipient_list = [user.email, ]
        send_mail(subject,
                          message,
                          email_from,
                          recipient_list)
        user1.isUsed=1
        user1.token=token
        user1.expired_time=expires
        user1.save()
        return Response('Mail has been sent to your registered mail id', status=status.HTTP_200_OK)

class Resetpassword(APIView):
    def post(self, request, Reset_link):
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')
        email, token = Reset_link.split('.')
        email = urlsafe_base64_decode(email).decode()
        user = User.objects.get(email=email)
        user1 = Link.objects.get(user_id=user.id)
        if user1.isUsed == 0:
            return Response({'error':'You already have used the token'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password and confirm_new_password:
            return Response({'error':'Please provide the fields new_password and confirm_new_password'}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() > user1.expired_time:
            print(timezone.now())
            return Response({'error':'The token has exxpired'}, status=status.HTTP_400_BAD_REQUEST)
        if token != user1.token:
            return Response({'error':'Wrong token provided'})
        if new_password != confirm_new_password:
            return Response({'error':'Your new_password and confirm_new_password do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        if token == user1.token and timezone.now() < user1.expired_time:
            print(timezone.now())
            user.password = make_password(new_password)
            user.save()
            user1.isUsed = 0
            user1.save()
            return Response('Password changed successfully.', status=status.HTTP_200_OK)



        
