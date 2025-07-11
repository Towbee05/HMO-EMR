from rest_framework import serializers
from accounts.models import User, Plans, Coverage
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
        # print(validated_data)
        user = User.objects.create(
            email = validated_data["email"],
            full_name = validated_data['full_name'],
        )
        if validated_data['password1'] == validated_data['password2']:
            user.set_password(validated_data['password1'])
            user.save()
        else:
            return ValidationError(_("Passwords don't matich"))
        return validated_data

class UserRegistrationPlanSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(min_length=11, max_length=11)
    password1 = serializers.CharField(max_length=20, write_only= True, min_length=6)
    password2 = serializers.CharField(max_length=20, write_only= True, min_length=6)
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "full_name", "gender", "phone_number", "password1", "password2"]
    def validate(self, attrs):
        #Creating a regex expression to validate the phone number as Nigerian
        regex = r'^((\+?234)\s?|0)(((7)0)|((8|9)(0|1)))\d{8}'
        phone_number = attrs.get('phone_number')
        matched = re.match(regex, phone_number)
        if matched:
            pass
        else:
            raise ValueError(_("Not a valid phone number"))
        return super().validate(attrs)
    
    def create(self, validated_data):
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

    class Meta:
        model = User
        fields = ['email', 'password'] #, 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context['request']
        user = authenticate(request, username= email, password= password)
        if user is None:
            raise AuthenticationFailed('Invalid Credentials')

        return attrs

class PlanSerializer(serializers.ModelSerializer):
    coverage = serializers.PrimaryKeyRelatedField(queryset= Coverage.objects.all(), many=True)
    class Meta:
        model = Plans
        fields = ['id', 'name', 'coverage', 'price', 'status']
    def validate_name(self, value):
        if Plans.objects.filter(name__iexact = value).exists():
            raise ValidationError(_("Plan with name already exists!"))
        return value
    def update(self, instance, validated_data):
        name = validated_data.get('name') or None
        price = validated_data.get('price') or None
        status = validated_data.get('status') or None
        coverage = validated_data.get('coverage') or None
        id = instance.id
        if name is not None:
            instance.name = name
        if price is not None:
            instance.price = price
        if status is not None:
            instance.status = status
        if coverage is not None:
            instance.coverage.set(coverage)

        instance.save()
        return instance
    def create(self, validated_data):
        coverage = validated_data.pop('coverage')
        print(validated_data)
        plan = Plans.objects.create(**validated_data)
        plan.coverage.set(coverage)
        return plan

class CoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = '__all__'


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta: 
        model = User
        fields = ['old_password', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError(_(f"Passwords must be equal"))
        return data
    def validate_oldpassword(self, value):
        print(self)
        user = self.context['request'].user
        print(user.check_password(value))
        if not user.check_password(value):
            raise ValidationError(_("Entered Password does not match that in db"))
        return value
    def update(self, instance, validated_data):
        print('UPDATE', instance)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'display_picture']

    def validate_email(self, value):
        if User.objects.filter(email__iexact = value).exists():
            raise ValidationError(_('Email already exist in db'))
        return value
    
    def validate_name(self, value):
        if User.objects.filter(full_name__iexact = value).exists():
            raise ValidationError(_(f"User with name {value} already exist",))
        
        return value
    
    def update(self, instance, validated_data):
        email = validated_data.get('email') or None
        full_name = validated_data.get('full_name') or None
        display = validated_data.get('display_picture') or None
        if email is not None:
            instance.email = email
        if full_name is not None:
            instance.full_name = full_name
        if display is not None:
            instance.display_picture = display
        instance.save()
        return instance