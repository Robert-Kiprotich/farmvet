from rest_framework.permissions import BasePermission

class Is_Vet(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_vet_officer

class Is_Farmer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_farmer

class Is_Official(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_official
    
