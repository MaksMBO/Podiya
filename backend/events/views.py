from rest_framework import generics, permissions, response, status
from .serializers import TagSerializer
from .models import Tag


class IsAdminContentMakerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow administrators to edit or delete tags.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff or request.user.is_superuser or request.user.is_content_maker


# ---------------------------------------TAGS--------------------------------------------------------
class TagBaseView(generics.GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminContentMakerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_content_maker:
            return Tag.objects.all()
        return Tag.objects.none()

    def perform_action(self, serializer):
        serializer.save()


class TagListCreateView(TagBaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        self.perform_action(serializer)


class TagRetrieveUpdateDestroyView(TagBaseView, generics.RetrieveUpdateDestroyAPIView):
    def perform_update(self, serializer):
        self.perform_action(serializer)

# -----------------------------------------------------------------------------------------------


# ---------------------------------------EVENTS--------------------------------------------------------


# -----------------------------------------------------------------------------------------------


# ---------------------------------------COMMENTS--------------------------------------------------------


# -----------------------------------------------------------------------------------------------
