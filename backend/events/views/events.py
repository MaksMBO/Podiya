from datetime import timedelta, datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from events.models import Event, City, Review
from events.serializers import EventSerializer, EventUpdateSerializer, ReviewSerializerGet, ReviewSerializerPost
from helper import check_datetime_format
from helper.custom_permission import IsAdminContentMakerOrReadOnly
from helper.paginator import EventPagination

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly & IsAdminContentMakerOrReadOnly]
    pagination_class = EventPagination

    def get_serializer_class(self):
        if self.action == 'update':
            return EventUpdateSerializer
        return EventSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        required_keys = ['name', 'description', 'price', 'image', 'city', 'location_info', 'time']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return Response(
                {"error": f"Missing keys: {', '.join(missing_keys)}"}, status=status.HTTP_400_BAD_REQUEST)

        city = get_object_or_404(City, id=data['city'])

        try:
            new_event = Event.objects.create(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                image=data['image'],
                city=city,
                location_info=data['location_info'],
                time=data['time'],
                creator=request.user
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        tags = [tag.strip() for tag in data.get('tags', '').split(",") if tag.strip()]
        new_event.tags.add(*tags)

        serializer = EventSerializer(new_event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        tags = data.get('tags', '').split(",")

        try:
            instance.name = data.get('name', instance.name)
            instance.description = data.get('description', instance.description)
            instance.image = data.get('image', instance.image)
            instance.time = data.get('time', instance.time)

            if tags != ['']:
                instance.tags.clear()
                instance.tags.add(*tags)

            instance.save()

            serializer = EventUpdateSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        queryset = Event.objects.all()
        query_params = self.request.query_params

        filters = {
            'name__icontains': query_params.get('search'),
            'time__gte': query_params.get('date_from'),
            'time__lte': query_params.get('date_to'),
            'price__gte': query_params.get('price_from'),
            'price__lte': query_params.get('price_to'),
            'city__name': query_params.get('city')
        }

        for key, value in filters.items():
            if value is not None:
                if 'date' in key and not check_datetime_format.validate_datetime_format(value):
                    raise ValidationError({"error": f"{key} input format is incorrect"})
                if 'price' in key and not value.isdigit():
                    raise ValidationError({"error": f"Invalid input for '{key}', must be an integer"})
                queryset = queryset.filter(**{key: value})

        sort = query_params.get('sort')
        if sort in ['price_asc', 'price_desc']:
            queryset = queryset.order_by(f'{"-" if sort == "price_desc" else ""}price')

        tags = query_params.get('tags')
        if tags is not None:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset

    @action(detail=False, methods=['GET'], pagination_class=EventPagination)
    def by_user(self, request):
        events = Event.objects.filter(creator=request.user)
        page = self.paginate_queryset(events)
        serializer = EventSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['GET'], pagination_class=EventPagination)
    def current_week_events(self, request):
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)

        start_of_week = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        end_of_week = timezone.make_aware(datetime.combine(end_of_week, datetime.max.time()))

        events = Event.objects.filter(time__range=[start_of_week, end_of_week])

        page = self.paginate_queryset(events)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

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
