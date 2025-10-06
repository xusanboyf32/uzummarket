
import re
# BU DEFAULT AUTHDAN , BASIC ORQALI YOZILDI
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email')


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        #"""Email formatini tekshirish"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',value):
            raise serializers.ValidationError("Iltimos, to'g'ri email manzilini kiriting!")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email manzil band!")

        return value


    def validate(self, data):
        #"""Parollar mosligini tekshirish"""

        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Parollar mos kelmadi")

        email = data['email']
        password = data['password']
        # Bu username va password kombinatsiyasi bormi?
        all_users = User.objects.all()
        for user in all_users:
            if  user.email == email and check_password(password, user.password):

                raise serializers.ValidationError(
                    "Bu email va password kombinatsiyasi allaqachon mavjud! Boshqa password tanlang."
                )

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username:
            raise serializers.ValidationError("Username kiritishingiz kerak!")

        if not password:
            raise serializers.ValidationError("Parol kiritishingiz kerak!")

        if not email:
            raise serializers.ValidationError("Email kiritishingiz kerak!")


        users = User.objects.filter(username=username)

        if users.exists():
            # Passwordni tekshiramiz
            user_found = None
            for user in users:
                if user.email == email and check_password(password, user.password):
                    user_found = user
                    break


            if user_found:
                if user_found.is_active:
                    # Authenticate qilamiz
                    auth_user = authenticate(username=username, password=password)
                    if auth_user:
                        data['user'] = auth_user
                    else:
                        raise serializers.ValidationError("Authentication xatolik!")
                else:
                    raise serializers.ValidationError("Foydalanuvchi faol emas!")
            else:
                raise serializers.ValidationError("Login yoki parol xato!")
        else:
            raise serializers.ValidationError("Login yoki parol xato!")

        return data
