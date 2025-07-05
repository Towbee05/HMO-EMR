from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hospitals.views import HospitalViewset

router = DefaultRouter()
router.register(r'', HospitalViewset, basename='hospitals')

urlpatterns = [
    path('', include(router.urls))
]
