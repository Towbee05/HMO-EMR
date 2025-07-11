from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from patients.models import Patients
from patients.serializers import PatientSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsSuperuser, IsHospital
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    authentication_classes = [ TokenAuthentication ]
    permission_classes = [IsAuthenticated, IsHospital, IsSuperuser]

    def get_queryset(self):
        queryset = Patients.objects.all()
        search = self.request.query_params.get('search')
        if search and search != ' ':
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