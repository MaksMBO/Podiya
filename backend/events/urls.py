from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.cities import CityDetail, CityList
from .views.tags import TagListCreateView, TagRetrieveUpdateDestroyView, TagListView
from .views.events import EventViewSet

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = [
    path(r'tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path(r'tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update'),
    path(r'tags/by_rating/', TagListView.as_view(), name='rating-tag-list'),
    path('cities/', CityList.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
    path(r'', include(router.urls)),
]
