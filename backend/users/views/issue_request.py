from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from users.models import IssueRequest
from users.serializers.issue_request import IssueRequestSerializer
from helper.paginator import EventPagination


class IssueRequestViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    ViewSet for handling issue requests.
    """
    queryset = IssueRequest.objects.all()
    serializer_class = IssueRequestSerializer
    pagination_class = EventPagination

    def perform_create(self, serializer):
        """
        Performs actions after creating an issue request.
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Returns the appropriate permissions for each action.
        """
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
