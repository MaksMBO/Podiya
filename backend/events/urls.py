from django.urls import path
from .views import TagListCreateView, TagRetrieveUpdateView

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagRetrieveUpdateView.as_view(), name='tag-retrieve-update'),
]
