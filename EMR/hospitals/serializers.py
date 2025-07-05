from rest_framework import serializers
from hospitals.models import Hospitals
from datetime import datetime
from accounts.models import Plans

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
        # 'location', 'status', 'email', 'phone', 'services', 'plans', 'accredition_license', 'accredition_status', 'accredition_expires', 'password'
        # fields = '__all__'
        
        # def create(self, validated_data):
        #     validated_data['plans']
        #     print(validated_data)
        #     if isinstance(validated_data['accredition_expires'], str):
        #         validated_data['accredition_expires'] = datetime.strptime(validated_data['accredition_expires'], "%Y-%m-%d")
        #     return super().create(validated_data)
        
        # def update(self, instance, validated_data):
        #     if 'accredition_expires' in validated_data and isinstance(validated_data['accredition_expires'], str):
        #         validated_data['accredition_expires'] = datetime.strptime(validated_data['accredition_expires'], "%Y-%m-%d")
        #     return super().update(instance, validated_data)