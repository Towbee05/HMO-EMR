from rest_framework import serializers
from patients.models import Patients
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import Plans

class PatientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only= True)
    password = serializers.CharField(min_length=6, max_length=20, write_only= True)
    plan = serializers.PrimaryKeyRelatedField(queryset= Plans.objects.all(), many=False)
    class Meta:
        model = Patients
        fields = ['id', 'name', 'age', 'email', 'phone', 'plan', 'status', 'password']

    def validate_name(self, value):
        if Patients.objects.filter(name__iexact = value).exists() or User.objects.filter(full_name__iexact = value).exists():
            raise ValidationError(_(f"Name: \"{value}\" is already in use"))
        return value
    
    def validate_email(self, value):
        if Patients.objects.filter(name__iexact = value).exists() or User.objects.filter(email__iexact = value).exists():
            raise ValidationError(_(f"Email: \"{value}\" is already in use"))
        return value
    
    def validate_phone(self, value):
        if Patients.objects.filter(phone__iexact= value).exists():
            raise ValidationError(_(f"Phone: \"{value}\" is already in use"))
        return value
    
    def validate_age(self, value):
        if value < 18:
            raise ValidationError(_(f"Age: \"{value}\" is too low!!"))
        return value
    
    def update(self, instance, validated_data):
        name = validated_data.get('name') or None
        age = validated_data.get('age') or None
        email = validated_data.get('email') or None
        phone = validated_data.get('phone') or None
        plan = validated_data.get('plan') or None
        status = validated_data.get('status') or None

        id= instance.id
        user = instance.user

        if name is not None:
            instance.name = name
            user.full_name = name
        if email is not None:
            instance.email = email
            user.email = email
        if age is not None:
            instance.age = age
        if phone is not None:
            instance.phone = phone
        if plan is not None:
            instance.plan = plan
        if status is not None:
            instance.status = status

        instance.save()
        user.save()
        return instance

    def create(self, validated_data):
        patient = Patients.objects.create(
            name= validated_data['name'],
            age= validated_data['age'],
            email = validated_data['email'],
            phone = validated_data['phone'],
            plan = validated_data['plan'],
            status = validated_data['status']
        )
        user, created = User.objects.get_or_create(email= validated_data['email'])
        if created:
            user.full_name = validated_data['name']
            user.password = make_password(validated_data['password'])
            user.save()
        patient.user = user
        patient.save()
        return validated_data