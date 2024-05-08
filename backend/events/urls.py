from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagListCreateView, TagRetrieveUpdateDestroyView, EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update'),
    path('', include(router.urls)),
]
