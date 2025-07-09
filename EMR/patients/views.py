from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from patients.models import Patients
from patients.serializers import PatientSerializer
from rest_framework import status
# Create your views here.

class PatientViewSet(ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer

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