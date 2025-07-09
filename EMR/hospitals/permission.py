from rest_framework.permissions import BasePermission
from hospitals.models import Hospitals

# class IsHospital(BasePermission):
#     def has_permission (self, request, view):
#         user_email = request.user.email
#         return Hospitals.objects.filter(email = user_email).exists()
    