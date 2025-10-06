
################################################

from django.urls import path
from .views import (
    # API Views
    SignUpView, SignInView, SignOutView, ProfileView, CheckAuthView,
    # HTML Views
    login_page, register_page, profile_page, logout_page
)

urlpatterns = [
    # ==================== API ENDPOINTS ====================
    path('api/signup/', SignUpView.as_view(), name='api_signup'),
    path('api/signin/', SignInView.as_view(), name='api_signin'),
    path('api/signout/', SignOutView.as_view(), name='api_signout'),
    path('api/profile/', ProfileView.as_view(), name='api_profile'),
    path('api/check-auth/', CheckAuthView.as_view(), name='api_check_auth'),

    # ==================== HTML PAGES ====================
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('profile/', profile_page, name='profile_page'),
    path('logout/', logout_page, name='logout_page'),
]
