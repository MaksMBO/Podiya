from rest_framework import permissions, viewsets
from .serializers import UserSerializer
from .models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
