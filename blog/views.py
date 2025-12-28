from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Tag, Post
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostSerializer,
    PostListSerializer
)


# Category Views
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


# Tag Views
class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


# Post Views
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'tags', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'views']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        # Filter by published status for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset.select_related('author', 'category').prefetch_related('tags')


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Post.objects.all()
        # Filter by published status for non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset.select_related('author', 'category').prefetch_related('tags')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views for published posts
        if instance.status == 'published':
            instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostByCategory(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        queryset = Post.objects.filter(category__slug=category_slug)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset.select_related('author', 'category').prefetch_related('tags')


class PostByTag(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        queryset = Post.objects.filter(tags__slug=tag_slug)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset.select_related('author', 'category').prefetch_related('tags').distinct()


class PostByAuthor(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        author_id = self.kwargs['pk']
        queryset = Post.objects.filter(author_id=author_id)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset.select_related('author', 'category').prefetch_related('tags')
