from datetime import timedelta

from django.db.models import Q
from rest_framework import generics, permissions, response, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from helper import check_datetime_format
from helper.paginator import EventPagination
from .serializers import TagSerializer, EventSerializer, EventUpdateSerializer, ReviewSerializerGet, \
    ReviewSerializerPost
from .models import Tag, Event, Review, City
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
    pagination_class = EventPagination
    pagination_class.page_size = 12

    def get_serializer_class(self):
        if self.action == 'update':
            return EventUpdateSerializer
        return EventSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        tags = data.get('tags', '').split(",")

        new_event = Event.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=data['image'],
            city=City.objects.get(id=data['city']),
            location_info=data['location_info'],
            time=data['time'],
            creator=request.user
        )

        new_event.tags.add(*tags)

        serializer = EventSerializer(new_event)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        tags = data.get('tags', '').split(",")

        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)
        instance.price = data.get('price', instance.price)
        instance.image = data.get('image', instance.image)
        instance.city = City.objects.get(id=data.get('city', instance.city.id))
        instance.location_info = data.get('location_info', instance.location_info)
        instance.time = data.get('time', instance.time)
        instance.creator = request.user

        instance.tags.clear()
        instance.tags.add(*tags)

        instance.save()

        serializer = EventSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Event.objects.all()
        search_param = self.request.query_params.get('search', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        price_from = self.request.query_params.get('price_from', None)
        price_to = self.request.query_params.get('price_to', None)
        sort = self.request.query_params.get('sort', None)
        tags = self.request.query_params.get('tags', None)
        city = self.request.query_params.get('city', None)

        if search_param is not None:
            queryset = queryset.filter(Q(name__icontains=search_param))

        if date_from:
            if not check_datetime_format.validate_datetime_format(date_from):
                raise ValidationError({"error": "Некоректний формат вводу дати"})

            queryset = queryset.filter(time__gte=date_from)

        if date_to:
            if not check_datetime_format.validate_datetime_format(date_to):
                raise ValidationError({"error": "Некоректний формат вводу дати"})

            queryset = queryset.filter(time__lte=date_to)

        if price_from:
            if not price_from.isdigit():
                raise ValidationError({"error": "Недійсний ввід для 'price_from', має бути цілим числом"})

            queryset = queryset.filter(price__gte=price_from)

        if price_to:
            if not price_to.isdigit():
                raise ValidationError({"error": "Недійсний ввід для 'price_to', має бути цілим числом"})

            queryset = queryset.filter(price__lte=price_to)

        if sort is not None:
            if sort == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort == 'price_desc':
                queryset = queryset.order_by('-price')

        if tags is not None:
            tags = tags.split(',')
            for tag in tags:
                queryset = queryset.filter(tags__name=tag)

        if city is not None:
            queryset = queryset.filter(city__name=city)

        return queryset

    @action(detail=False, methods=['GET'])
    def by_user(self, request):
        events = Event.objects.filter(creator=request.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

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
