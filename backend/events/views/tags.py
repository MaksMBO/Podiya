from django.db.models import Avg, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import generics, permissions

from rest_framework.generics import ListAPIView

from events.models import Tag
from events.serializers import TagSerializer, RatingTagSerializer
from helper.custom_permission import IsAdminContentMakerOrReadOnly
from helper.paginator import EventPagination


class TagBaseView(generics.GenericAPIView):
    """
    Base class for performing operations on Tag instances.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminContentMakerOrReadOnly]

    def get_queryset(self):
        """
        Returns a queryset for the list of tags available to the user.
        """
        user = self.request.user
        if user.is_staff or user.is_content_maker:
            return Tag.objects.all()
        return Tag.objects.none()

    def perform_action(self, serializer):
        serializer.save()


class TagListCreateView(TagBaseView, generics.ListCreateAPIView):
    """
    Class for viewing and creating tags.
    """

    def perform_create(self, serializer):
        """
        Performs the action of saving a new tag.
        """
        self.perform_action(serializer)


class TagRetrieveUpdateDestroyView(TagBaseView, generics.RetrieveUpdateDestroyAPIView):
    """
    Class for updating, and deleting individual tags.
    """

    def perform_update(self, serializer):
        """
        Performs the action of updating an existing tag.
        """
        self.perform_action(serializer)


class TagListView(ListAPIView):
    """
    A simple ListAPIView for viewing tags.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = EventPagination
    serializer_class = RatingTagSerializer

    def get_queryset(self):
        """
        Return a list of all the existing tags, ordered by average rating.
        """
        return Tag.objects.annotate(
            average_rating=Coalesce(Avg('events__reviews__rating'), 0, output_field=DecimalField())
        ).order_by('-average_rating')
