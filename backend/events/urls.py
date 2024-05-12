from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.tags import TagListCreateView, TagRetrieveUpdateDestroyView, TagListView
from .views.events import EventViewSet

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = [
    path(r'tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path(r'tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update'),
    path(r'tags/by_rating/', TagListView.as_view(), name='rating-tag-list'),
    path(r'', include(router.urls)),
]
