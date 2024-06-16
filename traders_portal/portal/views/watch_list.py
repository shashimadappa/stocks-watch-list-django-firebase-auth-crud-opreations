from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import WatchList
from ..serializers.watch_list import WatchListSerializer
from django.shortcuts import get_object_or_404
from ..models import Users, Company
from ..config import authenticate_firebase_token

@api_view(['POST'])
def add_to_watchlist(request):
    
    token = request.headers.get('Authorization')
    auth_result = authenticate_firebase_token(token)
    if isinstance(auth_result, Response):
            return auth_result
    
    company_id = request.data.get('company_id')

    try:
        user = get_object_or_404(Users, id=auth_result.id)
        company = get_object_or_404(Company, id=company_id)
        
        watchlist_item, created = WatchList.objects.get_or_create(user=user, company=company)
        
        if created:
            serializer = WatchListSerializer(watchlist_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Company already exists in watchlist."}, status=status.HTTP_400_BAD_REQUEST)
    
    except Users.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Company.DoesNotExist:
        return Response({"message": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_watchlist(request, user_id):
    token = request.headers.get('Authorization')
    auth_result = authenticate_firebase_token(token)
    if isinstance(auth_result, Response):
            return auth_result
    try:
        user = get_object_or_404(Users, id=user_id)
        watchlist_items = WatchList.objects.filter(user=user)
        serializer = WatchListSerializer(watchlist_items, many=True)
        return Response(serializer.data)
    
    except Users.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_watchlist(request, watchlist_id):
    token = request.headers.get('Authorization')
    auth_result = authenticate_firebase_token(token)
    if isinstance(auth_result, Response):
            return auth_result
    user = request.user
    watchlist_item = get_object_or_404(WatchList, id=watchlist_id)
    
    if watchlist_item:
        watchlist_item.delete()
        return Response({"message": "Watchlist entry deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Watchlist entry not found."}, status=status.HTTP_404_NOT_FOUND)