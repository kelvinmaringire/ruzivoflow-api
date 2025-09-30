from django.urls import path
from content_api.views import (
    DocumentListCreate, DocumentRetrieveUpdateDestroy,
    ImageListCreate, ImageRetrieveUpdateDestroy,
    CollectionListCreate, CollectionRetrieveUpdateDestroy,
)

urlpatterns = [
    # Documents
    path('documents/', DocumentListCreate.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentRetrieveUpdateDestroy.as_view(), name='document-detail'),

    # Images
    path('images/', ImageListCreate.as_view(), name='image-list-create'),
    path('images/<int:pk>/', ImageRetrieveUpdateDestroy.as_view(), name='image-detail'),

    # Collections
    path('collections/', CollectionListCreate.as_view(), name='collection-list-create'),
    path('collections/<int:pk>/', CollectionRetrieveUpdateDestroy.as_view(), name='collection-detail'),
]
