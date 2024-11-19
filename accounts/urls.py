from django.urls import path, include
from accounts import views
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    path('google/token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('agree/', AgreeMentAPIView.as_view()),    
]