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
            instance.price = data.get('price', instance.price)
            instance.image = data.get('image', instance.image)
            instance.city = get_object_or_404(City, id=data.get('city', instance.city.id))
            instance.location_info = data.get('location_info', instance.location_info)
            instance.time = data.get('time', instance.time)
            instance.creator = request.user

            instance.tags.clear()
            instance.tags.add(*tags)

            instance.save()

            serializer = EventSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                raise ValidationError({"error": "Date input format is incorrect"})

            queryset = queryset.filter(time__gte=date_from)

        if date_to:
            if not check_datetime_format.validate_datetime_format(date_to):
                raise ValidationError({"error": "Date input format is incorrect"})

            queryset = queryset.filter(time__lte=date_to)

        if price_from:
            if not price_from.isdigit():
                raise ValidationError({"error": "Invalid input for 'price_from', must be an integer"})

            queryset = queryset.filter(price__gte=price_from)

        if price_to:
            if not price_to.isdigit():
                raise ValidationError({"error": "Invalid input for 'price_to', must be an integer"})

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
