from django.urls import path
from .views import TagListCreateView, TagRetrieveUpdateDestroyView

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update'),
]
