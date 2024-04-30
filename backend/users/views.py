from rest_framework import permissions, viewsets
from .serializers import CustomUserSerializer
from .models import CustomUser


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    #
    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = [permissions.AllowAny]
    #     elif self.action == 'list':
    #         self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    #     else:
    #         self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    #     return super(CustomUserViewSet, self).get_permissions()
