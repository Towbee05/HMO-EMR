from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class IsHospital(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff