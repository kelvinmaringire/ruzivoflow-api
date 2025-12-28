from django.urls import path

from .views import (
    CategoryListCreate,
    CategoryDetail,
    TagListCreate,
    TagDetail,
    PostListCreate,
    PostDetail,
    PostByCategory,
    PostByTag,
    PostByAuthor,
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetail.as_view(), name='category-detail'),

    # Tag URLs
    path('tags/', TagListCreate.as_view(), name='tag-list-create'),
    path('tags/<slug:slug>/', TagDetail.as_view(), name='tag-detail'),

    # Post URLs
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<slug:slug>/', PostDetail.as_view(), name='post-detail'),
    path('posts/category/<slug:slug>/', PostByCategory.as_view(), name='post-by-category'),
    path('posts/tag/<slug:slug>/', PostByTag.as_view(), name='post-by-tag'),
    path('posts/author/<int:pk>/', PostByAuthor.as_view(), name='post-by-author'),
]

