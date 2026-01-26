"""
API View Tests for Blog App

Crucial tests for Post API endpoints:
- Post creation via POST /blog/posts/
- Author auto-set from request.user
- Slug auto-generation
- Published status filtering for non-authenticated users
- Post update via PUT/PATCH /blog/posts/<slug>/
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from blog.models import Post, Category, Tag


class PostListCreateTestCase(APITestCase):
    """Test Post creation via POST /blog/posts/ endpoint"""

    def setUp(self):
        """Set up test client, user, and test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.tag = Tag.objects.create(name='Python')
        
        self.post_data = {
            'title': 'Test Post Title',
            'content': '<p>This is test content</p>',
            'excerpt': '<p>Test excerpt</p>',
            'category': self.category.id,
            'tags': [self.tag.id],
            'status': 'draft'
        }

    def test_create_post_authenticated(self):
        """Test post creation by authenticated user"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post('/blog/posts/', self.post_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        
        post = Post.objects.get(title='Test Post Title')
        # Verify author is auto-set from request.user
        self.assertEqual(post.author, self.user)
        # Verify slug is auto-generated
        self.assertIsNotNone(post.slug)
        self.assertEqual(post.slug, 'test-post-title')

    def test_create_post_unauthenticated(self):
        """Test that unauthenticated users cannot create posts"""
        response = self.client.post('/blog/posts/', self.post_data, format='json')
        
        # Should return 401 Unauthorized due to IsAuthenticatedOrReadOnly permission
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_list_posts_unauthenticated_only_published(self):
        """Test that unauthenticated users only see published posts"""
        self.client.force_authenticate(user=self.user)
        
        # Create published post
        published_data = self.post_data.copy()
        published_data['status'] = 'published'
        published_data['title'] = 'Published Post'
        self.client.post('/blog/posts/', published_data, format='json')
        
        # Create draft post
        draft_data = self.post_data.copy()
        draft_data['status'] = 'draft'
        draft_data['title'] = 'Draft Post'
        self.client.post('/blog/posts/', draft_data, format='json')
        
        # Unauthenticate and list posts
        self.client.force_authenticate(user=None)
        response = self.client.get('/blog/posts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see published post
        # Handle both paginated and non-paginated responses
        if 'results' in response.data:
            posts = response.data['results']
        else:
            posts = response.data if isinstance(response.data, list) else []
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Published Post')
        self.assertEqual(posts[0]['status'], 'published')

    def test_list_posts_authenticated_sees_all(self):
        """Test that authenticated users see all posts regardless of status"""
        self.client.force_authenticate(user=self.user)
        
        # Create published post
        published_data = self.post_data.copy()
        published_data['status'] = 'published'
        published_data['title'] = 'Published Post'
        self.client.post('/blog/posts/', published_data, format='json')
        
        # Create draft post
        draft_data = self.post_data.copy()
        draft_data['status'] = 'draft'
        draft_data['title'] = 'Draft Post'
        self.client.post('/blog/posts/', draft_data, format='json')
        
        # List posts as authenticated user
        response = self.client.get('/blog/posts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see both posts
        # Handle both paginated and non-paginated responses
        if 'results' in response.data:
            posts = response.data['results']
        else:
            posts = response.data if isinstance(response.data, list) else []
        self.assertEqual(len(posts), 2)
        titles = [post['title'] for post in posts]
        self.assertIn('Published Post', titles)
        self.assertIn('Draft Post', titles)


class PostDetailTestCase(APITestCase):
    """Test Post update via PUT/PATCH /blog/posts/<slug>/ endpoint"""

    def setUp(self):
        """Set up test client, user, and test post"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            category=self.category,
            content='<p>Original content</p>',
            excerpt='<p>Original excerpt</p>',
            status='draft'
        )

    def test_update_post_patch(self):
        """Test post partial update using PATCH"""
        self.client.force_authenticate(user=self.user)
        
        update_data = {'title': 'Updated Post Title', 'status': 'published'}
        
        response = self.client.patch(f'/blog/posts/{self.post.slug}/', update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post Title')
        self.assertEqual(self.post.status, 'published')
        # Other fields should remain unchanged
        self.assertEqual(self.post.content, '<p>Original content</p>')

    def test_retrieve_post_unauthenticated_draft(self):
        """Test that unauthenticated users cannot retrieve draft posts"""
        # Post is draft by default
        response = self.client.get(f'/blog/posts/{self.post.slug}/')
        
        # Should return 404 because draft posts are filtered out
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_post_increments_views(self):
        """Test that retrieving published post increments view count"""
        self.post.status = 'published'
        self.post.views = 0
        self.post.save()
        
        initial_views = self.post.views
        
        response = self.client.get(f'/blog/posts/{self.post.slug}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.post.refresh_from_db()
        # Views should be incremented
        self.assertEqual(self.post.views, initial_views + 1)
