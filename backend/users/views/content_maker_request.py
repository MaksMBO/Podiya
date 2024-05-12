from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import ContentMakerRequest
from users.serializers.content_maker_request import ContentMakerRequestSerializer, ContentMakerRequestUpdateSerializer
from helper.paginator import EventPagination


class ContentMakerRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling content maker requests.
    """
    queryset = ContentMakerRequest.objects.all()
    pagination_class = EventPagination

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.
        """
        if self.action in ['update', 'partial_update']:
            return ContentMakerRequestUpdateSerializer
        return ContentMakerRequestSerializer

    def perform_create(self, serializer):
        """
        Performs actions after creating a content maker request.
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Returns the appropriate permissions for each action.
        """
        if self.action in ['list', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
