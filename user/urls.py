from django.urls import path
from .views import UserListCreateView , MyTokenObtainPairView ,UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView 

urlpatterns = [
    # Authentication
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management superAdmin only
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-list'),
  
    
    
]