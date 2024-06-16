from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers.user import UserRegistrationSerializer, UsersSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Users
from ..config import authenticate_firebase_token, secret_key
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import jwt
from ..serializers.user import LoginSerializer

@api_view(['POST'])
def register_user(request):
    email = request.data['email']
    password = request.data['password']
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = Users.objects.get(email=email)
            
            if check_password(password, user.password):
                payload = {
                    'user_id': user.id,
                    'username': user.name
                }
                jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

                response_data = {
                'token': jwt_token,
                'username': user.email
                }
            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_users_by_id(request, id):
    token = request.headers.get('Authorization')
    auth_result = authenticate_firebase_token(token)
    if isinstance(auth_result, Response):
        return auth_result
    else:
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


