from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers.company import CompanySerializer
from ..models import Company
from ..config import authenticate_firebase_token

@api_view(['GET'])
def get_company_by_symbol(request, symbol):
    token = request.headers.get('Authorization')
    auth_result = authenticate_firebase_token(token)
    if isinstance(auth_result, Response):
            return auth_result
    company = get_object_or_404(Company, symbol=symbol)
    serializer = CompanySerializer(company)
    return Response(serializer.data, status=status.HTTP_200_OK)