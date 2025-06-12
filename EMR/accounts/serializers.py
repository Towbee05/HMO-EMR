from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.translation import gettext_lazy as _
import re

class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=20, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=20, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ["email", "full_name", "password1", "password2"]

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            email = validated_data["email"],
            full_name = validated_data['full_name'],
        )
        if validated_data['password1'] == validated_data['password2']:
            user.set_password(validated_data['password1'])
            user.save()
        
        else:
            return ValidationError(_("Passwords don't match"))

        return validated_data

class UserRegistrationPlanSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=11, max_length=11)
    password1 = serializers.CharField(max_length=20, write_only= True, min_length=6)
    password2 = serializers.CharField(max_length=20, write_only= True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "full_name", "gender", "phone_number", "password1", "password2"]

    def validate(self, attrs):
        print(attrs)
        #Creating a regex expression to validate the phone number as Nigerian
        regex = r'^((\+?234)\s?|0)(((7)0)|((8|9)(0|1)))\d{8}'
        phone_number = attrs.get('phone_number')
        matched = re.match(regex, phone_number)

        if matched:
            print(phone_number)
        else:
            raise ValueError(_("Not a valid phone number"))
        return super().validate(attrs)
    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            email = validated_data["email"],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            gender = validated_data['gender'],
            phone_number = validated_data['phone_number'],
            password1 = validated_data['password1'],
            password2 = validated_data['password2']
        )
        return validated_data

class HospitalRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=20, write_only= True, min_length=6)
    password2 = serializers.CharField(max_length=20, write_only= True, min_length=6)
    is_staff = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "gender", "phone_number", "password1", "password2", "is_staff"]

    def validate(self, attrs):
        pass
        return super().validate(attrs)
    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            email = validated_data["email"],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            gender = validated_data['gender'],
            phone_number = validated_data['phone_number'],
            password1 = validated_data['password1'],
            password2 = validated_data['password2'],
            is_staff = validated_data['is_staff']
        )
        return validated_data



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length= 256, min_length= 8)
    password = serializers.CharField(max_length = 60, min_length=6, write_only= True)
    access_token = serializers.CharField(max_length = 255, read_only= True)
    refresh_token = serializers.CharField(max_length = 255, read_only = True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print(attrs, email, password)
        request = self.context['request']
        user = authenticate(request, email= email, password= password)
        if user is None:
            raise AuthenticationFailed('Invalid Credentials')
        token = user.tokens()

        return {
            'email' : user.email,
            'full name' : user.full_name,
            'refresh_token' : str(token.get('refresh')),
            'access_token' : str(token.get('access'))
        }
