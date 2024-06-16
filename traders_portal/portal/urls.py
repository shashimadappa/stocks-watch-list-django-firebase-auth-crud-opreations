from django.urls import path
from .views.watch_list import add_to_watchlist, user_watchlist, delete_watchlist
from .views.user import register_user, login_user, get_users_by_id
from .views.company import get_company_by_symbol

from .views.user_by_firebase import register_user2, login_user2

urlpatterns = [
    # user
    path('user-register/', register_user, name='register_user'),
    path('usr-login/', login_user, name='login_user'),
    path('get-users/<int:id>', get_users_by_id, name='get_users_by_id'),
    
    # registers user in firebase and db
    path('user-register-firebase/', register_user2, name='register_user-firebase'),
    path('user-login-firebase/', login_user2, name='login_user-firebase'), #Generates session token from from firebase
    
    # watch list
    path('watch-list-add/', add_to_watchlist, name='watch_list_add/'),
    path('get-user-watch-list/<int:user_id>/', user_watchlist, name='get_user_watch_list'),
    path('watch-list-delete/<int:watchlist_id>/', delete_watchlist, name='delete_watchlist'),
    
    # company
    path('get-company-by-symbol/<str:symbol>/', get_company_by_symbol, name='get_company_by_symbol'),
]
