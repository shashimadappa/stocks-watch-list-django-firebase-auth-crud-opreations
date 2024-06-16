from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers.user import UserRegistrationSerializer, LoginSerializer
from ..models import Users
from ..config import authenticate, secret_key
from django.contrib.auth.hashers import check_password
import jwt
import firebase_admin
from firebase_admin import auth as firebase_auth
from ..config import firebase_admin

@api_view(['POST'])
def register_user2(request):
    email = request.data['email']
    password = request.data['password']
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            user_record = firebase_auth.create_user(
                uid=str(user.id),
                email=email,
                password=password
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user2(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = Users.objects.get(email=email)
            
            if check_password(password, user.password):
                user = firebase_auth.get_user_by_email(email)
                custom_token = firebase_auth.create_custom_token(user.uid)
                            
                response_data = {
                    'token': custom_token,
                    'email': user.email
                }
                return Response(response_data)
            else:
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
