from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .serializers import UserSerializer, SignUpSerializer, SignInSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                'success': True,
                'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tkazildi!',
                'user': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'success': True,
                'message': 'Login muvaffaqiyatli!',
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            'success': True,
            'message': 'Logout muvaffaqiyatli!'
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data
        })


class CheckAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user': UserSerializer(request.user).data
            })
        else:
            return Response({
                'authenticated': False
            })


# ==================== HTML VIEWS ====================
def login_page(request):
    """Login uchun HTML sahifa"""
    if request.user.is_authenticated:
        return redirect('/products/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username va parolni to'ldiring!")
            return render(request, 'auth/login.html')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Xush kelibsiz!")
            return redirect('/products/')
        else:
            messages.error(request, "Username yoki parol xato!")

    return render(request, 'auth/login.html')


def register_page(request):
    """Ro'yxatdan o'tish uchun HTML sahifa"""
    if request.user.is_authenticated:
        return redirect('/products/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not username or not password:
            messages.error(request, "Username va parolni to'ldiring!")
            return render(request, 'auth/register.html')

        if password != password_confirm:
            messages.error(request, "Parollar mos kelmadi!")
            return render(request, 'auth/register.html')

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu foydalanuvchi nomi band!")
                return render(request, 'auth/register.html')

            user = User.objects.create_user(
                username=username,
                password=password
            )
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli!")
            return redirect('/products/')

        except Exception as e:
            messages.error(request, f"Xato yuz berdi: {str(e)}")

    return render(request, 'auth/register.html')


def profile_page(request):
    """Profil uchun HTML sahifa"""
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    return render(request, 'auth/profile.html')


def logout_page(request):
    """Logout uchun"""
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz!")
    return redirect('/auth/login/')

