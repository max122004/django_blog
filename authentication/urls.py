from django.urls import path
from rest_framework.authtoken import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import Logout, UserCreateAPIView, UserListAPIView, UserDeleteAPIView, UserDetailAPIView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('list/', UserListAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('<int:pk>/delete/', UserDeleteAPIView.as_view())
]
