from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from hospitals.serializers import HospitalSerializers
from hospitals.models import Hospitals

# Create your views here.

class HospitalViewset(ModelViewSet):
    # queryset = Hospitals.objects.all()
    serializer_class = HospitalSerializers
    # lookup_field= 'name'

    def get_queryset(self):
        queryset = Hospitals.objects.all()
        # search = self.reques
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains = search)
        return queryset