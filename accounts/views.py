from django.shortcuts import render
from rest_framework import generics , permissions 
from .serializers import RegisterSerializer , ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Profile , User 
from django.core.mail import send_mail
from .tasks import send_otp_via_email
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.decorators import api_view, permission_classes




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        otp = user.generate_otp()
        send_otp_via_email.delay(user.email,user.username,otp)
        
        return Response({"message": "User registered successfully.Please check your email for the verification code."}, status=status.HTTP_201_CREATED)


class ResendOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user          # أو: user = self.request.user
        message = user.resend_otp()
        return Response({"message": message})

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.otp_code == otp:
            user.is_verified = True
            user.otp_code = None  # امسحي OTP بعد التحقق
            user.save()
            return Response({"message": "Account verified successfully!"}, status=200)
        else:
            return Response({"error": "Invalid OTP"}, status=400)

        
        
        
class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
