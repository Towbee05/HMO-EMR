from rest_framework import serializers
from hospitals.models import Hospitals
from datetime import datetime
from accounts.models import Plans
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.contrib.auth.hashers import make_password

class HospitalSerializers(serializers.ModelSerializer):
    id= serializers.UUIDField(read_only=True)
    plans = serializers.PrimaryKeyRelatedField(queryset= Plans.objects.all(), many=False)
    accredition_expires = serializers.DateField()
    password = serializers.CharField(min_length=6, max_length=20,write_only=True)
    class Meta:
        model = Hospitals
        fields = [
            'id', 'name', 'email', 'location', 'status', 'phone', 'services', 'plans', 'accredition_license', 'accredition_status', 'accredition_expires' , 'password'
        ]
        read_only_fields = ['id']

    def validate_name(self, value):
        if Hospitals.objects.filter(name__iexact= value).exists():
            raise ValidationError(_(f"Hospital with name: \"{value}\" already exists"))
        return value
    def validate_email(self, value):
        if Hospitals.objects.filter(email__iexact= value).exists() or User.objects.filter(email__iexact = value).exists():
            raise ValidationError(_(f"Email: \"{value}\" is already in use"))
        
        return value
    def validate_phone(self, value):
        if Hospitals.objects.filter(phone= value).exists():
            raise ValidationError(_(f"Phone: \"{value}\" is already in use"))
        return value
    
    def update(self, instance, validated_data):
        name = validated_data.get('name') or None
        email = validated_data.get('email') or None
        location = validated_data.get('location') or None
        status = validated_data.get('status') or None
        phone = validated_data.get('phone') or None
        services = validated_data.get('services') or None
        plans = validated_data.get('plans') or None
        accredition_license = validated_data.get('accredition_license') or None
        accredition_status = validated_data.get('accredition_status') or None
        accredition_expires = validated_data.get('accredition_expires') or None

        id = instance.id
        user = instance.user
        if name is not None:
            instance.name= name
            user.full_name= name
        if email is not None:
            instance.email= email
            user.email = email
        if location is not None:
            instance.location= location
        if status is not None:
            instance.status= status
        if phone is not None:
            instance.phone= phone
        if services is not None:
            instance.services= services
        if plans is not None:
            instance.plans= plans
        if accredition_license is not None:
            instance.accredition_license= accredition_license
        if accredition_status is not None:
            instance.accredition_status= accredition_status
        if accredition_expires is not None:
            instance.accredition_expires= accredition_expires
        
        instance.save()
        user.save()
        return instance

    def create(self, validated_data):
        hospital= Hospitals.objects.create(
            name= validated_data['name'],
            email= validated_data['email'],
            location= validated_data['location'],
            status= validated_data['status'],
            phone= validated_data['phone'],
            services= validated_data['services'],
            plans= validated_data['plans'],
            accredition_license = validated_data['accredition_license'],
            accredition_status = validated_data['accredition_status'],
            accredition_expires = validated_data['accredition_expires'],
        )
        user, created = User.objects.get_or_create(email= validated_data['email'])
        if created:
            user.full_name = validated_data['name']
            user.password = make_password(validated_data['password'])
            user.is_staff= True
            user.save()
        hospital.user= user
        hospital.save()
        return validated_data