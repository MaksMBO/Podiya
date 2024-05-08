from datetime import timedelta

from rest_framework import generics, permissions, response, status, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializer, EventSerializer, EventUpdateSerializer, ReviewSerializerGet, \
    ReviewSerializerPost
from .models import Tag, Event, Review
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action


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


# ---------------------------------------EVENTS/Comments--------------------------------------------------------
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly & IsAdminContentMakerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'update':
            return EventUpdateSerializer
        return EventSerializer

    @action(detail=False, methods=['GET'])
    def current_week_events(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        events = Event.objects.filter(time__range=[start_of_week, end_of_week])

        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        event = self.get_object()
        comments = Review.objects.filter(event=event)
        serializer = ReviewSerializerGet(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        event = self.get_object()
        serializer = ReviewSerializerPost(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------------------------


