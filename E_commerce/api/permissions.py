from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedAndSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET" or request.method == 'DELETE':
            print(request.user)
            if request.user.is_authenticated and (request.user == obj.user):
                return True
            else:
                return False

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (request.user.is_staff and request.user.is_authenticated):
            return True
        else:
            return False
            
