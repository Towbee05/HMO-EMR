from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from hospitals.serializers import HospitalSerializers
from hospitals.models import Hospitals
from rest_framework import status
from rest_framework.response import Response
# from accounts.permission import IsSuperAdmin

# Create your views here.

class HospitalViewset(ModelViewSet):
    # queryset = Hospitals.objects.all()
    serializer_class = HospitalSerializers
    # lookup_field= 'name'
    # permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        queryset = Hospitals.objects.all()
        # search = self.reques
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains = search)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        print(f"views : {instance}")
        data = self.serializer_class(instance).data
        response = super().partial_update(request, *args, **kwargs)
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user.delete()
        print(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)